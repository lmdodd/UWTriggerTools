/*
 * =====================================================================================
 *
 *       Filename:  puMultipTreeRegionEt.cc
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


class puMultipTreeRegionEt : public edm::EDAnalyzer {
	public:
		explicit puMultipTreeRegionEt(const edm::ParameterSet& pset);
		static const unsigned int N_TOWER_PHI;
		static const unsigned int N_TOWER_ETA;
	private:
		virtual void analyze(const edm::Event& evt, const edm::EventSetup& es);
		double egPhysicalEt(const L1CaloEmCand& cand) const {
			return egLSB_*cand.rank();
		}

		double regionPhysicalEt(const L1CaloRegion& cand) const {
			return regionLSB_*cand.et();
		}

		// Find information about observables in the annulus.  We define the annulus
		// as all regions around the central region, with the exception of the second
		// highest in ET, as this could be sharing the 2x1.
		// MIPS in annulus refers to number of regions in the annulus which have
		// their MIP bit set.
		// egFlags is the number where (!tauVeto && !mip)
		void findAnnulusInfo(int ieta, int iphi,
				const L1CaloRegionCollection& regions,
				double* associatedSecondRegionEt,
				double* associatedThirdRegionEt,
				unsigned int* mipsInAnnulus,
				unsigned int* egFlagsInAnnulus,
				unsigned int* mipInSecondRegion) const;
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
		float TPGH_;
		float TPGHtwr_;
		float TPGEtwr_;
		float TPG5x5_;
		float TPG5x5_gcteta_;
		float TPG5x5_tpgeta_;
		float TPGh5x5_;
		float TPGe5x5_;
		float TPG7x7_;
		float genEta_;
		int genRgnEta_;
		float genPhi_;
		unsigned int npvs_;

		float maxEg2x1Pt_;
		float maxEg2x1Pt_Delta_;

		float maxRegionPt_;
		float maxRegionPt_2ndPt_;
		float maxRegionPt_Delta_;
		int maxRegionPt_Eta_;
		int maxRegionPt_Phi_;
		int NZR_;

		Handle<L1CaloRegionCollection> newRegions;
		Handle<L1CaloEmCollection> newEMCands;
		Handle<LumiScalersCollection> lumiScalers;
		Handle<reco::VertexCollection> vertices;
		Handle<reco::GenParticleCollection> genParticle;
		Handle<EcalTrigPrimDigiCollection> ecal;
		Handle<HcalTrigPrimDigiCollection> hcal;

		vector<float> regionPt_;
		vector<int> regionEta_;
		vector<float> regionPhi_;

		vector<double> sinPhi;
		vector<double> cosPhi;

		int egammaSeed;
		bool ECALOn;
		double egLSB_;
		double regionLSB_;

		double LSB = 0.5;

		vector<vector<unsigned int>> eTowerETCode;
		vector<vector<unsigned int>> hTowerETCode;
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

//
// Given a region at iphi/ieta, find the highest region in the surrounding
// regions.
void puMultipTreeRegionEt::findAnnulusInfo(int ieta, int iphi,
		const L1CaloRegionCollection& regions,
		double* associatedSecondRegionEt,
		double* associatedThirdRegionEt,
		unsigned int* mipsInAnnulus,
		unsigned int* egFlagsInAnnulus,
		unsigned int* mipInSecondRegion) const {
	unsigned int neighborsFound = 0;
	unsigned int mipsCount = 0;
	unsigned int egFlagCount = 0;
	double highestNeighborEt = 0;
	// We don't want to count the contribution of the highest neighbor, this allows
	// us to subtract off the highest neighbor at the end, so we only loop once.
	bool highestNeighborHasMip = false;
	bool highestNeighborHasEGFlag = false;
	double secondNeighborEt = 0;
	for(L1CaloRegionCollection::const_iterator region = regions.begin();
			region != regions.end(); region++) {
		int regionPhi = region->gctPhi();
		int regionEta = region->gctEta();
		unsigned int deltaPhi = std::abs(deltaPhiWrapAtN(18, iphi, regionPhi));
		unsigned int deltaEta = std::abs(ieta - regionEta);
		if ((deltaPhi + deltaEta) > 0 && deltaPhi < 2 && deltaEta < 2) {
			double regionET = regionPhysicalEt(*region);
			if (regionET > highestNeighborEt) {
				if(highestNeighborEt!=0) secondNeighborEt=highestNeighborEt;
				highestNeighborEt = regionET;
				// Keep track of what flags the highest neighbor has
				highestNeighborHasMip = region->mip();
				highestNeighborHasEGFlag = !region->mip() && !region->tauVeto();
			}
			// count how many neighbors pass the flags.
			if (region->mip()) {
				mipsCount++;
			}
			if (!region->mip() && !region->tauVeto()) {
				egFlagCount++;
			}
			// If we already found all 8 neighbors, we don't need to keep looping
			// over the regions.
			neighborsFound++;
			if (neighborsFound == 8) {
				break;
			}
		}
	}
	// check if we need to remove the highest neighbor from the flag count.
	if (highestNeighborHasMip)
		mipsCount--;
	if (highestNeighborHasEGFlag)
		egFlagCount--;
	// set output
	*associatedSecondRegionEt = highestNeighborEt;
	*associatedThirdRegionEt =secondNeighborEt;
	*mipsInAnnulus = mipsCount;
	*mipInSecondRegion = highestNeighborHasMip;
	*egFlagsInAnnulus = egFlagCount;
}

unsigned int const puMultipTreeRegionEt::N_TOWER_PHI = 72;
unsigned int const puMultipTreeRegionEt::N_TOWER_ETA = 56;

puMultipTreeRegionEt::puMultipTreeRegionEt(const edm::ParameterSet& pset):
	eTowerETCode(N_TOWER_PHI, vector<unsigned int>(N_TOWER_ETA)),
	hTowerETCode(N_TOWER_PHI, vector<unsigned int>(N_TOWER_ETA))
{
	// Initialize the ntuple builder
	edm::Service<TFileService> fs;
	tree = fs->make<TTree>("Ntuple", "Ntuple");
	tree->Branch("regionPt", "std::vector<float>", &regionPt_);
	tree->Branch("regionEta", "std::vector<int>", &regionEta_);
	tree->Branch("maxRegionPt", &maxRegionPt_, "maxRegionPt/F");
	tree->Branch("maxRegionPt_2ndPt", &maxRegionPt_2ndPt_, "maxRegionPt_2ndPt/F");
	tree->Branch("maxRegionPt_Delta", &maxRegionPt_Delta_, "maxRegionPt_Delta/F");
	tree->Branch("maxRegionPt_Eta", &maxRegionPt_Eta_, "maxRegionPt_Eta/i");
	tree->Branch("maxRegionPt_Phi", &maxRegionPt_Phi_, "maxRegionPt_Phi/i");
	tree->Branch("NZR", &NZR_, "NZR/i");
	tree->Branch("maxEg2x1Pt", &maxEg2x1Pt_, "maxEg2x1Pt/F");
	tree->Branch("maxEg2x1Pt_Delta", &maxEg2x1Pt_Delta_, "maxEg2x1Pt_Delta/F");
	tree->Branch("TPGSum", &TPGSum_, "TPGSum/F");
	tree->Branch("TPGDiff", &TPGDiff_, "TPGDiff/F");
	tree->Branch("TPGHoE", &TPGHoE_, "TPGHoE/F");
	tree->Branch("TPGH", &TPGH_, "TPGH_/F");
	tree->Branch("TPGE", &TPGE_, "TPGE/F");
	tree->Branch("TPGHtwr", &TPGHtwr_, "TPGHtwr_/F");
	tree->Branch("TPGEtwr", &TPGEtwr_, "TPGEtwr_/F");
	tree->Branch("TPG5x5", &TPG5x5_, "TPG5x5_/F");
	tree->Branch("TPG5x5_gcteta", &TPG5x5_gcteta_, "TPG5x5_gcteta_/F");
	tree->Branch("TPG5x5_tpgeta", &TPG5x5_tpgeta_, "TPG5x5_tpgeta_/F");
	tree->Branch("TPGh5x5", &TPGh5x5_, "TPGh5x5_/F");
	tree->Branch("TPGe5x5", &TPGe5x5_, "TPGe5x5_/F");
	tree->Branch("TPG7x7", &TPG7x7_, "TPG7x7_/F");
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
	regionLSB_ = pset.getParameter<double>("regionLSB");
	egLSB_ = pset.getParameter<double>("egammaLSB");
	egammaSeed = pset.getParameter<int>("egammaSeed");
	ECALOn = pset.getParameter<bool>("ECALOn");
}


void puMultipTreeRegionEt::analyze(const edm::Event& evt, const edm::EventSetup& es) {

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
	regionEta_.clear();
	regionPt_.clear();
	//eTowerETCode.clear();

	maxRegionPt_Delta_ = 999;
	maxRegionPt_ = 0;
	maxRegionPt_Eta_ = -999;
	maxRegionPt_Phi_ = -999;
	maxRegionPt_2ndPt_ = 0;
	maxEg2x1Pt_ = 0;
	maxEg2x1Pt_Delta_ = 999;

	NZR_=0;

	TPGSum_ = 0;
	TPGDiff_ = 0;
	TPGHoE_ = 0;

	genPhi_ = -999;
	genPt_ = -9;
	genEta_ = -9;
	genRgnEta_ = -9;

	TPGE_ =0;
	TPGH_=0;

	TPGHtwr_=0;
	TPGEtwr_=0;

	TPG5x5_=0;
	TPG5x5_gcteta_=999;
	TPG5x5_tpgeta_=999;
	TPGh5x5_=0;
	TPGe5x5_=0;
	TPG7x7_=0;

	double maxObjDelta = 999;		
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

	std::cout << "TPGS" << std::endl;
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
		unsigned int et= (*ecal)[i].compressedEt()*LSB;
		TPGSum_ +=et;
		TPGE_ +=et;
		eTowerETCode[iphi][ieta] = et; 

		if (et>0){cout<<"eTowerETCode: "<<eTowerETCode[iphi][ieta]<<endl;}
		if ((*ecal)[i].compressedEt() > 0) {
			std::cout << "ecal eta/phi=" << ieta << "/" << iphi
				<< " = (" << getEtaTPG(cal_ieta) << "/" << getPhiTPG(cal_iphi) << ") "
				<< " et="<< (*ecal)[i].compressedEt()*egLSB_ << " fg=" << (*ecal)[i].fineGrain()
				<< " rctEta="<< twrEta2RegionEta(ieta) << " rctPhi=" << twrPhi2RegionPhi(cal_iphi)
				<< std::endl;
		}
		if (et>maxTPGEPt){
			maxTPGEPt=et;
			maxTPGEPt_phi = iphi; //this one starts at 0-72
			maxTPGEPt_eta = ieta; //this one is 0-54
		} 
	}
	ESHandle<L1CaloHcalScale> hcalScale;
	es.get<L1CaloHcalScaleRcd>().get(hcalScale);

	std::cout << "HCAL TPGS" << std::endl;
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

			if (energy > 0) {
				std::cout << "hcal eta/phi=" << ieta << "/" << iphi
					<< " = (" << getEtaTPG(ieta) << "/" << getPhiTPG(iphi) << ") "
					<< " et=" << (*hcal)[i].SOI_compressedEt()
					<< " energy=" << energy
					<< " rctEta="<< twrEta2RegionEta(hnieta) << " rctPhi=" << twrPhi2RegionPhi(hniphi)
					<< " fg=" << (*hcal)[i].SOI_fineGrain() << std::endl;
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
				TPGe5x5_ += eTowerETCode[tpgsquarephi][tpgsquareeta];		
				TPG5x5_ += hTowerETCode[tpgsquarephi][tpgsquareeta];	
				TPG5x5_ += eTowerETCode[tpgsquarephi][tpgsquareeta];		
			}
		}
	}


	//tpg 7x7 incomplete calculation
	if (maxTPGPt >0){
		for (int j = -3; j < 4; ++j) {//phi
			for (int k = -3; k < 4; ++k) { //eta
				int tpgsquarephi= maxTPGPt_phi+j;
				int tpgsquareeta= maxTPGPt_eta+k;	
				if (tpgsquarephi==-1) {tpgsquarephi=71;}
				if (tpgsquarephi==-2) {tpgsquarephi=70;}
				if (tpgsquarephi==-3) {tpgsquarephi=69;}
				if (tpgsquarephi==72) {tpgsquarephi=0;}
				if (tpgsquarephi==73) {tpgsquarephi=1;}
				if (tpgsquarephi==74) {tpgsquarephi=2;}
				if (tpgsquareeta>55 || tpgsquareeta<0) {continue;}//No Eta values beyond
				TPG7x7_ += hTowerETCode[tpgsquarephi][tpgsquareeta];	
				TPG7x7_ += eTowerETCode[tpgsquarephi][tpgsquareeta];		
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


	for(L1CaloEmCollection::const_iterator egtCand =
			newEMCands->begin();
			egtCand != newEMCands->end(); egtCand++){
		double eget = egPhysicalEt(*egtCand);
		if(eget > egammaSeed && eget > maxEg2x1Pt_)
		{
			maxEg2x1Pt_ = eget; 
			maxEg2x1Pt_Delta_ = genPt_-eget;
		}
	}//end egtCAnd



	for(L1CaloRegionCollection::const_iterator newRegion = newRegions->begin(); newRegion != newRegions->end(); newRegion++)
	{
		double regionET =  regionPhysicalEt(*newRegion);
		int regionEta = newRegion->gctEta(); 
		int regionPhi = newRegion->gctPhi(); 

		double regionEta_convert = convertRegionEta(regionEta);
		double regionPhi_convert = convertRegionPhi(regionPhi);

		double ObjDeltaPhi = deltaPhi(genPhi_, regionPhi_convert);
		double ObjDeltaEta = std::abs(genEta_ - regionEta_convert);
		double ObjDelta = sqrt((ObjDeltaPhi*ObjDeltaPhi)+(ObjDeltaEta*ObjDeltaEta));

		regionPt_.push_back(regionET);
		regionEta_.push_back(regionEta);

		if (regionET>0){ //>2
			NZR_ ++;
			double associatedSecondRegionEt = 0;
			double associatedThirdRegionEt = 0;
			unsigned int mipsInAnnulus = 0;
			unsigned int egFlagsInAnnulus = 0;
			unsigned int mipInSecondRegion = 0;
			findAnnulusInfo(regionEta, regionPhi,*newRegions,&associatedSecondRegionEt, &associatedThirdRegionEt, &mipsInAnnulus, &egFlagsInAnnulus, &mipInSecondRegion);
			//cout << "Associ. 2nd Pt: "<< associatedSecondRegionEt<<endl;

			//if (ObjDelta<.5 && genRgnEta_==regionEta && regionET==maxRegionPt_) 
			if (regionET>maxRegionPt_) 
			{       
				maxRegionPt_=regionET;
				maxRegionPt_Eta_=regionEta;
				maxRegionPt_Phi_=regionPhi;
				maxRegionPt_2ndPt_= associatedSecondRegionEt;
				maxRegionPt_Delta_=genPt_-regionET;
				maxObjDelta = ObjDelta;
			}
		}//end regionET>2(egseed)			


	}//end for

	if (maxRegionPt_>0)
	{ 
		//cout<<"If Match:"<<endl;
		//int maxTPGPt =0;
		//int maxTPGPt_phi = 999;
		//int maxTPGPt_eta = 999;
		int tpgEta;
		bool border = false;
		int iPhi=maxRegionPt_Phi_;
		int iEta=maxRegionPt_Eta_;
		TPGDiff_ = maxRegionPt_-TPGSum_;

		//                std::cout<<"REGION_ETA"<<iEta<<endl;
		//              std::cout<<"REGION_PHI"<<iPhi<<endl;
		for(int i = -1; i < 3; i++) {
			for(unsigned int j = 0; j < 4; j++) {
				if(iEta>10){tpgEta=TPGEtaRange((iEta-11)*4 +1+j);}//rgnindx 11-21 ->(1-28) Tpg eta
				else if(iEta<11){tpgEta=TPGEtaRange(-((10-iEta)*4 +1+j));}//rgnindx 0-10 ->
				// remember that region phi 1 has TPG phi 2, 3, 4, 5
				int tpgPhi = iPhi * 4 + i-1;
				if (tpgPhi<0) {tpgPhi=71+i;}
				int TPGet = hTowerETCode[tpgPhi][tpgEta];
				if (TPGet>0)
				{
					cout<<"        "<<endl;
					cout<<"TPGet:"<<TPGet<<endl;
					cout<<"maxTPGPT_:"<<maxTPGPt<<endl;
					cout<<"TPGEta:"<<tpgEta<<endl;
					cout<<"iEta:"<<iEta<<endl;
					cout<<"TPGPhi:"<<tpgPhi<<endl;
					cout<<"iPhi:"<<iPhi<<endl;
				}
				if (TPGet>maxTPGPt){
					maxTPGPt=TPGet;
					if( i==-1 || i==2 || j==0 ||j==3){border=true;}
				}//end if
			}//end for j
		}//end for i
		if (border == true ){
			//std::cout<<"border = true"<<endl;
			maxRegionPt_=0;
			maxRegionPt_Delta_ =999;
		} 
		//		if (iEta < 7 || iEta > 14){
		//			maxRegionPt_=0;
		//			maxRegionPt_Delta_ =999;
		//		}
		//NEW TRY
		//	if (maxObjDelta>.5){
		//		maxRegionPt_=0;
		//		maxRegionPt_Delta_ =999;
		//	}

	}//end maxRegionPt

	std::cout<<"maxRegionPt: "<<maxRegionPt_ <<std::endl;
	std::cout<<"maxRegionPt Eta: "<< maxRegionPt_Eta_<< std::endl;
	std::cout<<"maxRegionPt Phi: "<< maxRegionPt_Phi_<< std::endl;
	std::cout<<"Next Event"<<std::endl;
	tree->Fill();
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(puMultipTreeRegionEt);
