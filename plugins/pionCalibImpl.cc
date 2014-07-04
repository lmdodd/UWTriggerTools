/*
 * =====================================================================================
 *
 *       Filename:  pionCalibImpl.cc
 *
 *    Description:  
 *
 *         Author:  Laura Dodd, laura.dodd@cern.ch Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */
#include "L1Trigger/UWTriggerTools/interface/ExpressionNtuple.h"
#include "L1Trigger/UWTriggerTools/interface/L1RecoMatch.h"
#include "L1Trigger/UCT2015/interface/helpers.h"
#include "L1Trigger/UCT2015/interface/UCTCandidate.h"
#include <memory>
#include <math.h>
#include <vector>
#include <list>
#include <TTree.h>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/L1Trigger/interface/L1JetParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/Common/interface/DetSet.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloCollections.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloRegion.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloEmCand.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloRegionDetId.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Scalers/interface/LumiScalers.h"
#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/EcalDigi/interface/EcalDigiCollections.h"
#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "CondFormats/L1TObjects/interface/L1CaloHcalScale.h"
#include "CondFormats/DataRecord/interface/L1CaloHcalScaleRcd.h"
#include "FWCore/Framework/interface/ESHandle.h"


//typedef std::vector<edm::InputTag> VInputTag;
//typedef std::vector<unsigned int> PackedUIntCollection;


using namespace std;
using namespace edm;


class pionCalibImpl : public edm::EDAnalyzer {
	public:
		explicit pionCalibImpl(const edm::ParameterSet& pset);
		static const double N_TOWER_PHI;
		static const double N_TOWER_ETA;
	private:
		virtual void analyze(const edm::Event& evt, const edm::EventSetup& es);


		TTree* tree;
		unsigned int run_;
		unsigned int lumi_;
		unsigned long int event_;

		InputTag scalerSrc_;
		InputTag uctDigis_;
		InputTag pvSrc_;
		InputTag genSrc_;
		InputTag ecalSrc_;
		InputTag hcalSrc_;


		float instLumi_;
		float genPt_;
		float TPGSum_;
		float TPGDiff_;
		float TPGHoE_;
		float TPGE_;
		float cTPGE_;
		float TPGH_;
		float cTPGH_;
		float TPGHtwr_;
		float TPGEtwr_;
		float TPG5x5_;
		float cTPG5x5_;
		float TPG5x5_gcteta_;
		float TPG5x5_tpgeta_;
		float TPGh5x5_;
		float TPGe5x5_;
		float cTPGh5x5_;
		float cTPGe5x5_;
		float genEta_;
		int genRgnEta_;
		float genPhi_;
		unsigned int npvs_;

		vector<double> TPGSF1_;
		vector<double> TPGSF2_;
		vector<double> TPGSFp_;

		int NZR_;

		Handle<L1CaloRegionCollection> newRegions;
		Handle<L1CaloEmCollection> newEMCands;
		Handle<LumiScalersCollection> lumiScalers;
		Handle<reco::VertexCollection> vertices;
		Handle<reco::GenParticleCollection> genParticle;
		Handle<EcalTrigPrimDigiCollection> ecal;
		Handle<HcalTrigPrimDigiCollection> hcal;


		vector<double> sinPhi;
		vector<double> cosPhi;

		int egammaSeed;
		bool ECALOn;
		double egLSB_;
		double regionLSB_;

		double LSB = 0.5;

		vector<vector<double>> eTowerETCode;
		vector<vector<double>> eCorrTowerETCode;
		vector<vector<double>> hTowerETCode;
		vector<vector<double>> hCorrTowerETCode;
};

//double getPhiTPG(int iPhi) {
	// TPG iPhi starts at 1 and goes to 72.  Let's index starting at zero.
//	return convertTPGPhi(iPhi-1);
//}

//int TPGEtaRange(int ieta){
//	unsigned int iEta = 0;
	// So here, -28 becomes 0.  -1 be comes 27.  +1 becomes 28. +28 becomes 55.
	// And we have mapped [-28, -1], [1, 28] onto [0, 55]   
//	if(ieta < 0)
//		iEta = ieta + 28;
//	else if(ieta > 0)
//		iEta = ieta + 27;
//	return iEta;
//}

//double getEtaTPG(int ieta) {
//	unsigned int iEta = 0;
//	// So here, -28 becomes 0.  -1 be comes 27.  +1 becomes 28. +28 becomes 55.
//	// And we have mapped [-28, -1], [1, 28] onto [0, 55]
//
//	if(ieta < 0)
//		iEta = ieta + 28;
//	else if(ieta > 0)
//		iEta = ieta + 27;
//	return convertTPGEta(iEta);
//}

double const pionCalibImpl::N_TOWER_PHI = 72;
double const pionCalibImpl::N_TOWER_ETA = 56;

pionCalibImpl::pionCalibImpl(const edm::ParameterSet& pset):
	eTowerETCode(N_TOWER_PHI, vector<double>(N_TOWER_ETA)),
	eCorrTowerETCode(N_TOWER_PHI, vector<double>(N_TOWER_ETA)),
	hTowerETCode(N_TOWER_PHI, vector<double>(N_TOWER_ETA)),
	hCorrTowerETCode(N_TOWER_PHI, vector<double>(N_TOWER_ETA))
{
	// Initialize the ntuple builder
	edm::Service<TFileService> fs;
	tree = fs->make<TTree>("Ntuple", "Ntuple");
	tree->Branch("NZR", &NZR_, "NZR/i");
	tree->Branch("TPGSum", &TPGSum_, "TPGSum/F");
	tree->Branch("TPGDiff", &TPGDiff_, "TPGDiff/F");
	tree->Branch("TPGHoE", &TPGHoE_, "TPGHoE/F");
	tree->Branch("TPGH", &TPGH_, "TPGH_/F");
	tree->Branch("cTPGH", &cTPGH_, "cTPGH_/F");
	tree->Branch("TPGE", &TPGE_, "TPGE/F");
	tree->Branch("cTPGE", &cTPGE_, "cTPGE/F");
	tree->Branch("TPG5x5", &TPG5x5_, "TPG5x5_/F");
	tree->Branch("cTPG5x5", &cTPG5x5_, "cTPG5x5_/F");
	tree->Branch("TPG5x5_gcteta", &TPG5x5_gcteta_, "TPG5x5_gcteta_/F");
	tree->Branch("TPG5x5_tpgeta", &TPG5x5_tpgeta_, "TPG5x5_tpgeta_/F");
	tree->Branch("TPGh5x5", &TPGh5x5_, "TPGh5x5_/F");
	tree->Branch("cTPGh5x5", &cTPGh5x5_, "cTPGh5x5_/F");
	tree->Branch("TPGe5x5", &TPGe5x5_, "TPGe5x5_/F");
	tree->Branch("cTPGe5x5", &cTPGe5x5_, "cTPGe5x5_/F");
	tree->Branch("genPt", &genPt_, "genPt/F");
	tree->Branch("genEta", &genEta_, "genEta/F");
	tree->Branch("genRgnEta", &genRgnEta_, "genRgnEta/i");
	tree->Branch("run", &run_, "run/i");
	tree->Branch("lumi", &lumi_, "lumi/i");
	tree->Branch("evt", &event_, "evt/l");
	tree->Branch("npvs", &npvs_, "npvs/i");
	tree->Branch("instlumi", &instLumi_, "instlumi/F");
	scalerSrc_ = pset.exists("scalerSrc") ? pset.getParameter<InputTag>("scalerSrc") : InputTag("scalersRawToDigi");
	genSrc_ = pset.exists("genSrc") ? pset.getParameter<InputTag>("genSrc") : InputTag("genParticles");
	// UCT variables
	pvSrc_ = pset.exists("pvSrc") ? pset.getParameter<InputTag>("pvSrc") : InputTag("offlinePrimaryVertices");
	ecalSrc_ = pset.exists("ecalSrc") ? pset.getParameter<InputTag>("ecalSrc"): InputTag("ecalDigis:EcalTriggerPrimitives");
	hcalSrc_ = pset.exists("hcalSrc") ? pset.getParameter<InputTag>("hcalSrc"): InputTag("hackHCALMIPs");
	TPGSF1_= pset.getParameter<vector<double> >("TPGSF1");
	TPGSF2_= pset.getParameter<vector<double> >("TPGSF2");
	TPGSFp_= pset.getParameter<vector<double> >("TPGSFp");
	regionLSB_ = pset.getParameter<double>("regionLSB");
	egLSB_ = pset.getParameter<double>("egammaLSB");
	egammaSeed = pset.getParameter<int>("egammaSeed");
	ECALOn = pset.getParameter<bool>("ECALOn");
}


void pionCalibImpl::analyze(const edm::Event& evt, const edm::EventSetup& es) {

	// Setup meta info
	run_ = evt.id().run();
	lumi_ = evt.id().luminosityBlock();
	event_ = evt.id().event();

	// Get instantaneous lumi from the scalers
	// thx to Carlo Battilana
	//Handle<LumiScalersCollection> lumiScalers;
	//Handle<L1CaloRegionCollection> newRegions;
	//edm::DetSetVector<L1CaloRegionCollection> newRegion;
	//edm::Handle<L1CaloRegionCollection>::const_iterator newRegion;

	evt.getByLabel(scalerSrc_, lumiScalers);
	evt.getByLabel("uctDigis", newRegions);
	evt.getByLabel("uctDigis", newEMCands);
	evt.getByLabel(pvSrc_, vertices);
	evt.getByLabel(genSrc_, genParticle);  
	evt.getByLabel(ecalSrc_, ecal);
	evt.getByLabel(hcalSrc_, hcal);

	// EVENT INFO 
	instLumi_ = -1;
	npvs_ = 0;

	npvs_ = vertices->size();

	if (lumiScalers->size())
		instLumi_ = lumiScalers->begin()->instantLumi();

	//Reset important things

	NZR_=0;

	TPGSum_ = 0;
	TPGDiff_ = 0;
	TPGHoE_ = 0;

	genPhi_ = -999;
	genPt_ = -9;
	genEta_ = -9;
	genRgnEta_ = -9;

	TPGE_ =0;
	cTPGE_ =0;
	TPGH_=0;
	cTPGH_=0;

	cTPG5x5_=0;
	cTPGh5x5_=0;
	cTPGe5x5_=0;

	TPG5x5_=0;
	TPG5x5_gcteta_=999;
	TPG5x5_tpgeta_=999;
	TPGh5x5_=0;
	TPGe5x5_=0;

	// TPG TEST
	float maxTPGPt = 0;
	float maxTPGEPt = 0;
	float maxTPGHPt = 0;
	int maxTPGPt_phi = 999;
	int maxTPGHPt_phi = 999;
	int maxTPGEPt_phi = 999;
	int maxTPGPt_eta = 999;
	int maxTPGHPt_eta = 999;
	int maxTPGEPt_eta = 999;

//	std::cout << "TPGS" << std::endl;
	//	std::cout << "ECAL TPGS" << std::endl;
	for (size_t i = 0; i < ecal->size(); ++i) {
		int cal_ieta = (*ecal)[i].id().ieta();
		int cal_iphi = (*ecal)[i].id().iphi();
		int iphi = cal_iphi-1;
		int ieta = TPGEtaRange(cal_ieta);
		// TPG iPhi starts at 1 and goes to 72.  Let's index starting at zero.
		// TPG ieta ideal goes from 0-55.
		//cout<<"Before filling eTower"
		//	<<"ieta:"<<ieta<<" cal_ieta:"<< cal_ieta<<" iphi:"<<iphi<<endl;
		double et= (*ecal)[i].compressedEt()*LSB;
		TPGSum_ +=et;
		TPGE_ +=et;
		eTowerETCode[iphi][ieta] = et; 
		int etbin;
	
		if(et<10){etbin=0;}
		else if(et<15){etbin=1;}
		else if(et<20){etbin=2;}
		else if(et<25){etbin=3;}
		else if(et<30){etbin=4;}
		else if(et<35){etbin=5;}
		else if(et<40){etbin=6;}
		else if(et<45){etbin=7;}
		else {etbin=8;}

		double alpha = TPGSF1_[etbin*56+ieta]; //v1


		//v2 v3
		//double alpha = TPGSF1_[etbin*56+ieta]*TPGSF2_[ieta];
	
	
		eCorrTowerETCode[iphi][ieta] = alpha*et;
		cTPGE_ +=alpha*et;
//		if (et>0){cout<<"eTowerETCode: "<<eTowerETCode[iphi][ieta]<<endl;}
		if ((*ecal)[i].compressedEt() > 0) {
//			std::cout << "ecal eta/phi=" << ieta << "/" << iphi
//				<< " = (" << getEtaTPG(cal_ieta) << "/" << getPhiTPG(cal_iphi) << ") "
//				<< " et="<< (*ecal)[i].compressedEt()*egLSB_ << " fg=" << (*ecal)[i].fineGrain()
//				<< " rctEta="<< twrEta2RegionEta(ieta) << " rctPhi=" << twrPhi2RegionPhi(cal_iphi)
//				<< std::endl;
		}
		if (et>maxTPGEPt){
			maxTPGEPt=et;
			maxTPGEPt_phi = iphi; //this one starts at 0-72
			maxTPGEPt_eta = ieta; //this one is 0-54
		} 
	}
	ESHandle<L1CaloHcalScale> hcalScale;
	es.get<L1CaloHcalScaleRcd>().get(hcalScale);

//	std::cout << "HCAL TPGS" << std::endl;
	for (size_t i = 0; i < hcal->size(); ++i) {
		int ieta = (*hcal)[i].id().ieta();
		int iphi = (*hcal)[i].id().iphi();
		int hniphi = iphi-1;
		int hnieta = TPGEtaRange(ieta);
		short absieta = std::abs((*hcal)[i].id().ieta());
		short zside = (*hcal)[i].id().zside();

		if (ieta >= -1000 && ieta <= 1000 &&
				iphi >= -1000 && ieta <= 1000) {
			double energy = hcalScale->et(
					(*hcal)[i].SOI_compressedEt(), absieta, zside); //*LSB

			hTowerETCode[hniphi][hnieta] = energy;
			TPGSum_ +=energy;
			TPGH_ += energy;
			int hetbin;
			//p

			if(energy<10){hetbin=0;}
			else if(energy<15){hetbin=1;}
			else if(energy<20){hetbin=2;}
			else if(energy<25){hetbin=3;}
			else if(energy<30){hetbin=4;}
			else if(energy<35){hetbin=5;}
			else if(energy<40){hetbin=6;}
			else if(energy<45){hetbin=7;}
			else {hetbin=8;}
			double alpha_h = 1; //v1 v2
		//	double alpha_h = TPGSFp_[hetbin*56+hnieta]; //v3
			hCorrTowerETCode[hniphi][hnieta] = alpha_h*energy;

			if (energy > 0) {
				//				std::cout << "hcal eta/phi=" << ieta << "/" << iphi
				//					<< " = (" << getEtaTPG(ieta) << "/" << getPhiTPG(iphi) << ") "
				//					<< " et=" << (*hcal)[i].SOI_compressedEt()
				//					<< " energy=" << energy
				//					<< " rctEta="<< twrEta2RegionEta(hnieta) << " rctPhi=" << twrPhi2RegionPhi(hniphi)
				//					<< " fg=" << (*hcal)[i].SOI_fineGrain() << std::endl;
			}
			if (energy>maxTPGHPt){
				maxTPGHPt=energy;
				maxTPGHPt_phi = hniphi; //this one starts at 0-72
				maxTPGHPt_eta = hnieta; //this one is 0-54
			} 
		}
	}//end HCAL TPG
	//if(ECALOn || maxTPGEPt>maxTPGHPt){
	if(ECALOn || maxTPGHPt<maxTPGEPt){
		maxTPGPt = maxTPGEPt;
		maxTPGPt_phi= maxTPGEPt_phi;
		maxTPGPt_eta= maxTPGEPt_eta;
	} 
	else{
		maxTPGPt = maxTPGHPt;
		maxTPGPt_phi= maxTPGHPt_phi;
		maxTPGPt_eta= maxTPGHPt_eta;
	}

	// tpg5x5 calculation

	if (maxTPGPt >0){
		TPG5x5_gcteta_ = twrEta2RegionEta(maxTPGPt_eta);
		TPG5x5_tpgeta_ = maxTPGPt_eta;
		for (int j = -2; j < 3; ++j) {//phi
			for (int k = -2; k < 3; ++k) { //eta
				int tpgsquarephi= maxTPGPt_phi+j;
				int tpgsquareeta= maxTPGPt_eta+k;	
				if (tpgsquarephi==-1) {tpgsquarephi=71;}
				if (tpgsquarephi==-2) {tpgsquarephi=70;}
				if (tpgsquarephi==72) {tpgsquarephi=0;}
				if (tpgsquarephi==73) {tpgsquarephi=1;}
				if (tpgsquareeta>55 || tpgsquareeta<0) {continue;}//No Eta values beyond
				TPGh5x5_ += hTowerETCode[tpgsquarephi][tpgsquareeta];		
				cTPGh5x5_ += hCorrTowerETCode[tpgsquarephi][tpgsquareeta];		
				TPGe5x5_ += eTowerETCode[tpgsquarephi][tpgsquareeta];		
				cTPGe5x5_ += eCorrTowerETCode[tpgsquarephi][tpgsquareeta];		
				TPG5x5_ += hTowerETCode[tpgsquarephi][tpgsquareeta];	
				TPG5x5_ += eTowerETCode[tpgsquarephi][tpgsquareeta];		
				cTPG5x5_ += hCorrTowerETCode[tpgsquarephi][tpgsquareeta];	
				cTPG5x5_ += eCorrTowerETCode[tpgsquarephi][tpgsquareeta];		
			}
		}
	}







	TPGHoE_ = TPGH_/TPGE_;

	for(reco::GenParticleCollection::const_iterator genparticleit = genParticle->begin(); genparticleit != genParticle->end(); genparticleit++)
	{// cout<<genparticleit->pdgId()<<"    "<<genparticleit->status()<<"    "<<genparticleit->pt()<<"    "<<genparticleit->eta()<<endl;
		genPt_ = genparticleit->pt();
		genEta_ = genparticleit->eta();
		genRgnEta_ = convertGenEta(genEta_);
		genPhi_ = genparticleit->phi();
	}	


	tree->Fill();
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(pionCalibImpl);
