//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon Mar 10 23:11:38 2014 by ROOT version 5.34/02
// from TTree Ntuple/Expression Ntuple
// found on file: h2tau.root
//////////////////////////////////////////////////////////

#ifndef Jet_h
#define Jet_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

// Fixed size dimensions of array or collections stored in the TTree if any.

class Jet {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Float_t         evt;
   Float_t         index;
   Float_t         l1DPhi;
   Float_t         l1DR;
   Float_t         l1Eta;
   Float_t         l1Match;
   Float_t         l1Phi;
   Float_t         l1Pt;
   Float_t         l1Type;
   Float_t         l1gDEta;
   Float_t         l1gDPhi;
   Float_t         l1gDR;
   Float_t         l1gEta;
   Int_t           l1gEtaCode;
   Float_t         l1gMatch;
   Float_t         l1gPU;
   Float_t         l1gPUUIC;
   Float_t         l1gPhi;
   Int_t           l1gPhiCode;
   Float_t         l1gPt;
   Float_t         l1gRegionEt;
   Float_t         lumi;
   Float_t         nPVs;
   Float_t         nRecoObjects;
   Float_t         recoEta;
   Float_t         recoPhi;
   Float_t         recoPt;
   Float_t         run;
   Int_t           idx;

   // List of branches
   TBranch        *b_evt;   //!
   TBranch        *b_index;   //!
   TBranch        *b_l1DPhi;   //!
   TBranch        *b_l1DR;   //!
   TBranch        *b_l1Eta;   //!
   TBranch        *b_l1Match;   //!
   TBranch        *b_l1Phi;   //!
   TBranch        *b_l1Pt;   //!
   TBranch        *b_l1Type;   //!
   TBranch        *b_l1gDEta;   //!
   TBranch        *b_l1gDPhi;   //!
   TBranch        *b_l1gDR;   //!
   TBranch        *b_l1gEta;   //!
   TBranch        *b_l1gEtaCode;   //!
   TBranch        *b_l1gMatch;   //!
   TBranch        *b_l1gPU;   //!
   TBranch        *b_l1gPUUIC;   //!
   TBranch        *b_l1gPhi;   //!
   TBranch        *b_l1gPhiCode;   //!
   TBranch        *b_l1gPt;   //!
   TBranch        *b_l1gRegionEt;   //!
   TBranch        *b_lumi;   //!
   TBranch        *b_nPVs;   //!
   TBranch        *b_nRecoObjects;   //!
   TBranch        *b_recoEta;   //!
   TBranch        *b_recoPhi;   //!
   TBranch        *b_recoPt;   //!
   TBranch        *b_run;   //!
   TBranch        *b_idx;   //!

   Jet(TTree *tree=0);
   virtual ~Jet();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef Jet_cxx
Jet::Jet(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/afs/hep.wisc.edu/cms/mcepeda/UCTANALYSISEMULATOR/UCT62XLaura/src/L1Trigger/UCT2015/test/h2tau.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("/afs/hep.wisc.edu/cms/mcepeda/UCTANALYSISEMULATOR/UCT62XLaura/src/L1Trigger/UCT2015/test/h2tau.root");
      }
      TDirectory * dir = (TDirectory*)f->Get("/afs/hep.wisc.edu/cms/mcepeda/UCTANALYSISEMULATOR/UCT62XLaura/src/L1Trigger/UCT2015/test/h2tau.root:/jetEfficiency");
      dir->GetObject("Ntuple",tree);

   }
   Init(tree);
}

Jet::~Jet()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t Jet::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t Jet::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void Jet::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("evt", &evt, &b_evt);
   fChain->SetBranchAddress("index", &index, &b_index);
   fChain->SetBranchAddress("l1DPhi", &l1DPhi, &b_l1DPhi);
   fChain->SetBranchAddress("l1DR", &l1DR, &b_l1DR);
   fChain->SetBranchAddress("l1Eta", &l1Eta, &b_l1Eta);
   fChain->SetBranchAddress("l1Match", &l1Match, &b_l1Match);
   fChain->SetBranchAddress("l1Phi", &l1Phi, &b_l1Phi);
   fChain->SetBranchAddress("l1Pt", &l1Pt, &b_l1Pt);
   fChain->SetBranchAddress("l1Type", &l1Type, &b_l1Type);
   fChain->SetBranchAddress("l1gDEta", &l1gDEta, &b_l1gDEta);
   fChain->SetBranchAddress("l1gDPhi", &l1gDPhi, &b_l1gDPhi);
   fChain->SetBranchAddress("l1gDR", &l1gDR, &b_l1gDR);
   fChain->SetBranchAddress("l1gEta", &l1gEta, &b_l1gEta);
   fChain->SetBranchAddress("l1gEtaCode", &l1gEtaCode, &b_l1gEtaCode);
   fChain->SetBranchAddress("l1gMatch", &l1gMatch, &b_l1gMatch);
   fChain->SetBranchAddress("l1gPU", &l1gPU, &b_l1gPU);
   fChain->SetBranchAddress("l1gPUUIC", &l1gPUUIC, &b_l1gPUUIC);
   fChain->SetBranchAddress("l1gPhi", &l1gPhi, &b_l1gPhi);
   fChain->SetBranchAddress("l1gPhiCode", &l1gPhiCode, &b_l1gPhiCode);
   fChain->SetBranchAddress("l1gPt", &l1gPt, &b_l1gPt);
   fChain->SetBranchAddress("l1gRegionEt", &l1gRegionEt, &b_l1gRegionEt);
   fChain->SetBranchAddress("lumi", &lumi, &b_lumi);
   fChain->SetBranchAddress("nPVs", &nPVs, &b_nPVs);
   fChain->SetBranchAddress("nRecoObjects", &nRecoObjects, &b_nRecoObjects);
   fChain->SetBranchAddress("recoEta", &recoEta, &b_recoEta);
   fChain->SetBranchAddress("recoPhi", &recoPhi, &b_recoPhi);
   fChain->SetBranchAddress("recoPt", &recoPt, &b_recoPt);
   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("idx", &idx, &b_idx);
   Notify();
}

Bool_t Jet::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void Jet::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t Jet::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef Jet_cxx
