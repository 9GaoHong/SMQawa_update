from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea.lookup_tools import extractor
from coffea.jetmet_tools import FactorizedJetCorrector
from coffea.jetmet_tools import JetResolution
from coffea.jetmet_tools import JECStack
from coffea.jetmet_tools import JetCorrectionUncertainty
from coffea.jetmet_tools import JetResolutionScaleFactor
from coffea.jetmet_tools import CorrectedJetsFactory
from coffea.jetmet_tools import CorrectedMETFactory

from coffea.lookup_tools import dense_lookup
import awkward as ak
import numpy as np
import os


jec_name_map = {
    'JetPt': 'pt',
    'JetMass': 'mass',
    'JetEta': 'eta',
    'JetA': 'area',
    'ptRaw': 'pt_raw',
    'massRaw': 'mass_raw',
    'Rho': 'rho',
    'METpt': 'pt',
    'METphi': 'phi',
    'JetPhi': 'phi',
    'UnClusteredEnergyDeltaX': 'MetUnclustEnUpDeltaX',
    'UnClusteredEnergyDeltaY': 'MetUnclustEnUpDeltaY',
}

def update_collection(event, coll):
    out = event
    for name, value in coll.items():
        out = ak.with_field(out, value, name)
    return out


def add_jme_variables(jets, events_rho):
    jets['pt_raw'  ] = (1 - jets.rawFactor) * jets.pt * (1- jets.muonSubtrFactor)
    jets['mass_raw'] = (1 - jets.rawFactor) * jets.mass * (1- jets.muonSubtrFactor)
    if hasattr(jets, 'matched_gen'):
        jets['pt_gen'  ] = ak.values_astype(ak.fill_none(jets.matched_gen.pt, 0), np.float32)
    else:
        jets['pt_gen'] = ak.Array(np.zeros(len(jets), dtype=np.float32))
    jets['rho'     ] = ak.broadcast_arrays(events_rho, jets.pt)[0]
    return jets

class JMEUncertainty:
    def __init__(
        self,
        jec_tag: str = 'Summer19UL18_V5_MC',
        jer_tag: str = 'Summer19UL18_JRV2_MC',
        era: str = "2018",
        is_mc: bool = True
    ):
        _data_path = os.path.join(os.path.dirname(__file__), 'data/jme/')
        extract = extractor()
        extract_L1 = extractor()
        extract_forjetCUT = extractor()
        
        correction_list = [
            # Jet Energy Correction
            f'* * {_data_path}/{era}/{jec_tag}_L1FastJet_AK4PFchs.jec.txt',
            f'* * {_data_path}/{era}/{jec_tag}_L2L3Residual_AK4PFchs.jec.txt',
            f'* * {_data_path}/{era}/{jec_tag}_L2Relative_AK4PFchs.jec.txt',
            f'* * {_data_path}/{era}/{jec_tag}_L3Absolute_AK4PFchs.jec.txt',
        ]
        
        correction_list_L1 = [
            # Jet Energy Correction
            f'* * {_data_path}/{era}/{jec_tag}_L1FastJet_AK4PFchs.jec.txt',
        ]
        correction_list_forjetCUT = [
            f'* * {_data_path}/{era}/{jec_tag}_L1FastJet_AK4PFchs.jec.txt',
            f'* * {_data_path}/{era}/{jec_tag}_L2L3Residual_AK4PFchs.jec.txt',
            f'* * {_data_path}/{era}/{jec_tag}_L2Relative_AK4PFchs.jec.txt',
            f'* * {_data_path}/{era}/{jec_tag}_L3Absolute_AK4PFchs.jec.txt',
            # Jet Energy Correction
        ]
        if is_mc:
            common_files = [    
                # Jet Energy Resolution
                f'* * {_data_path}/{era}/RegroupedV2_{jec_tag}_UncertaintySources_AK4PFchs.junc.txt',
                f'* * {_data_path}/{era}/{jer_tag}_PtResolution_AK4PFchs.jr.txt',
                f'* * {_data_path}/{era}/{jer_tag}_SF_AK4PFchs.jersf.txt',
            ]
            correction_list += common_files
            correction_list_L1 += common_files
            correction_list_forjetCUT += common_files
        jec_name_map.update({'ptGenJet': 'pt_gen'})
        extract_L1.add_weight_sets(correction_list_L1)
        extract_L1.finalize()
        evaluator_L1 = extract_L1.make_evaluator()
        jec_inputs_L1 = {
            name: evaluator_L1[name] for name in dir(evaluator_L1)
        }
        self.jec_stack_L1 = JECStack(jec_inputs_L1)
        self.jec_factory_L1 = CorrectedJetsFactory(jec_name_map, self.jec_stack_L1)
        
        extract_forjetCUT.add_weight_sets(correction_list_forjetCUT)
        extract_forjetCUT.finalize()
        evaluator_forjetCUT = extract_forjetCUT.make_evaluator()
        jec_inputs_forjetCUT = {
            name: evaluator_forjetCUT[name] for name in dir(evaluator_forjetCUT)
        }
        self.jec_stack_forjetCUT = JECStack(jec_inputs_forjetCUT)
        self.jec_factory_forjetCUT = CorrectedJetsFactory(jec_name_map, self.jec_stack_forjetCUT)
        
        extract.add_weight_sets(correction_list)
        extract.finalize()
        evaluator = extract.make_evaluator()
        jec_inputs = {
            name: evaluator[name] for name in dir(evaluator)
        }
        self.jec_stack = JECStack(jec_inputs)
        self.jec_factory = CorrectedJetsFactory(jec_name_map, self.jec_stack)
        self.met_factory = CorrectedMETFactory(jec_name_map)

    def corrected_jets(self, jets, event_rho, lazy_cache):
        jets_L123 = self.jec_factory.build(
            add_jme_variables(jets, event_rho),
            lazy_cache #events.caches[0]
        )
        jets_L1 = self.jec_factory_L1.build(
            add_jme_variables(jets, event_rho),
            lazy_cache #events.caches[0]
        )
        # print("jets_L123 ",jets_L123.pt[5493])
        # print("jets_L1",jets_L1.pt[5493])
        emFraction = jets_L123.chEmEF + jets_L123.neEmEF
        mask_jec = (jets_L123['pt'] > 15) & (emFraction <= 0.9)
        selected_jets_L123 = ak.mask(jets_L123, mask_jec)
        jets_shift = selected_jets_L123
        sj_L123, cj_L123 = np.sin(selected_jets_L123.phi), np.cos(selected_jets_L123.phi)
        sj_L1, cj_L1 = np.sin(jets_L1.phi), np.cos(jets_L1.phi)
        x = selected_jets_L123['pt'] * cj_L123 - jets_L1['pt'] * cj_L1
        y = selected_jets_L123['pt'] * sj_L123 - jets_L1['pt'] * sj_L1
        jets_shift['pt'] = np.hypot(x, y)
        jets_shift['phi'] = np.arctan2(y, x)
        return jets_shift

    def corrected_jets_jec(self, jets, event_rho, lazy_cache):
        jets = add_jme_variables(jets, event_rho)
        jets['pt_raw'  ] = jets.pt 
        jets['mass_raw'] = jets.mass 
        return self.jec_factory_forjetCUT.build(
            jets,
            lazy_cache #events.caches[0]
        )
    def corrected_met(self, met, jets, event_rho, lazy_cache):
        return self.met_factory.build(
            met,
            add_jme_variables(jets, event_rho),
            lazy_cache=lazy_cache # events.caches[0]
        )
