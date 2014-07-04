#define Jet_cxx
#include "Jet.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

TH1F*   DoEffi(Jet &t, Long64_t nentries,TString Name,double threshold, double etaMAX,  int N);
TH1F*   DoEffiOld(Jet &t, Long64_t nentries,TString Name,double threshold,double etaMAX, int N);

void doThePlots();
void printThePlots();

void plotEffisMultiJet(bool preparePlots=true){

	if (preparePlots) doThePlots();
	else printThePlots();

}

void doThePlots(){

	TFile *file= new TFile("/nfs_scratch/laura/05-04-RegionOffest_eff.root","READONLY");
        TTree* tree = (TTree*)file->Get("jetEfficiency/Ntuple");
        Long64_t entries=tree->GetEntries();
        Jet  treeTrigger;
        treeTrigger.Init(tree);

        TH1F *leadJetNew=DoEffi(treeTrigger, entries,"leadJetNew",40,3.,1); leadJetNew->SetLineColor(kBlue);
        TH1F *leadJetOld=DoEffiOld(treeTrigger, entries,"leadJetOld",40,3.,1); leadJetOld->SetLineColor(kRed);

        TH1F *secondJetNew=DoEffi(treeTrigger, entries,"secondJetNew",40,3.,2); secondJetNew->SetLineColor(kBlue);
        TH1F *secondJetOld=DoEffiOld(treeTrigger, entries,"secondJetOld",40,3.,2); secondJetOld->SetLineColor(kRed);

        TH1F *thirdJetNew=DoEffi(treeTrigger, entries,"thirdJetNew",40,3.,3); thirdJetNew->SetLineColor(kBlue);
        TH1F *thirdJetOld=DoEffiOld(treeTrigger, entries,"thirdJetOld",40,3.,3); thirdJetOld->SetLineColor(kRed);

        TH1F *fourthJetNew=DoEffi(treeTrigger, entries,"fourthJetNew",40,3.,4); fourthJetNew->SetLineColor(kBlue);
        TH1F *fourthJetOld=DoEffiOld(treeTrigger, entries,"fourthJetOld",40,3.,4); fourthJetOld->SetLineColor(kRed);

TCanvas *c1 = new TCanvas("c1","Root Canvas 1");
fourthJetNew->Draw("");
fourthJetOld->Draw("same");
c1->Print("4th Jet Efficiency");

	TFile *outfile=new TFile("effisJets40.root","RECREATE");
	leadJetNew->Write();
	leadJetOld->Write();
        secondJetNew->Write();
        secondJetOld->Write();
        thirdJetNew->Write();
        thirdJetOld->Write();
        fourthJetNew->Write();
        fourthJetOld->Write();
	file->Close();

}

TH1F*   DoEffi(Jet &t, Long64_t nentries,TString Name,double threshold, double etaMAX,int N)
{

   const int nbins=25;
   double ptbins[26];
         ptbins[0]=0;
        for (int i=0; i<26; i++){
                if (i==0) ptbins[i]=0;
                else if (i<4) ptbins[i]=ptbins[i-1]+5;
                else if(i<12) ptbins[i]=ptbins[i-1]+1;
                else if (i<20) ptbins[i]=ptbins[i-1]+2;
                else if (i<22) ptbins[i]=ptbins[i-1]+10;
                else if (i<26) ptbins[i]=ptbins[i-1]+50;
	}



   TH1F *Num= new TH1F(Name,"",nbins,ptbins); Num->Sumw2();
   TH1F *Den= new TH1F("Den"+Name,"",nbins,ptbins); Den->Sumw2();

   printf("Entries: %4lld \n",nentries);


   Long_t run=0, event=0;
   int count=0;

   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = t.LoadTree(jentry);

      if (ientry < 0) break;

      t.GetEntry(jentry);

      if(t.run!=run || t.evt!=event){
                run=t.run; event=t.evt;
                count=0;
      }
      if(fabs(t.recoEta)>etaMAX) continue;	

      count++;
      if(count!=N) continue;
      //count++;

      Den->Fill(t.recoPt);
      if(t.l1gMatch&&t.l1gPt>threshold) Num->Fill(t.recoPt);		
   }

  Num->Divide(Den); 

   return Num;
}


TH1F*   DoEffiOld(Jet &t, Long64_t nentries,TString Name,double threshold, double etaMAX, int N)
{

   const int nbins=25;
   double ptbins[26];
	 ptbins[0]=0;
	for (int i=0; i<26; i++){
		if (i==0) ptbins[i]=0; 
                else if (i<4) ptbins[i]=ptbins[i-1]+5;
                else if(i<12) ptbins[i]=ptbins[i-1]+1;
                else if (i<20) ptbins[i]=ptbins[i-1]+2;
                else if (i<22) ptbins[i]=ptbins[i-1]+10;
                else if (i<26) ptbins[i]=ptbins[i-1]+50;

	}


   TH1F *Num= new TH1F(Name,"",nbins,ptbins); Num->Sumw2();
   TH1F *Den= new TH1F("Den"+Name,"",nbins,ptbins); Den->Sumw2();

   printf("Entries: %4lld \n",nentries);

   Long_t run=0, event=0;
   int count=0;

   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = t.LoadTree(jentry);

      if (ientry < 0) break;

      t.GetEntry(jentry);

      if(t.run!=run || t.evt!=event){
		run=t.run; event=t.evt;
		count=0;
      }
      if(fabs(t.recoEta)>etaMAX) continue;

      count++;
      if(count!=N) continue;

      Den->Fill(t.recoPt);
      if(t.l1Match&&t.l1Pt>threshold) 	Num->Fill(t.recoPt);            
   }

  Num->Divide(Den); 

   return Num;
}
