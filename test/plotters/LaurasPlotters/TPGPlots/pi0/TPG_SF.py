'''
Usage:python jetEfficiencyPlot.py RootFile.root label[optional]
Author: L. Dodd, UW Madison
'''

from subprocess import Popen
from sys import argv, exit, stdout, stderr

import ROOT

# So things don't look like crap.
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

######## File #########
if len(argv) < 4:
   print 'Usage:python file.py RootFile20.root RootFile30.root RootFile40.root RootFile50.root Folder[optional]'
   exit()

infile_10 = argv[1]
infile_15 = argv[2]
infile_20 = argv[3]
infile_25 = argv[4]
infile_30 = argv[5]
infile_35 = argv[6]
infile_40 = argv[7]
infile_45 = argv[8]
infile_50 = argv[9]

ntuple_file_10 = ROOT.TFile(infile_10)
ntuple_file_15 = ROOT.TFile(infile_15)
ntuple_file_20 = ROOT.TFile(infile_20)
ntuple_file_25 = ROOT.TFile(infile_25)
ntuple_file_30 = ROOT.TFile(infile_30)
ntuple_file_35 = ROOT.TFile(infile_35)
ntuple_file_40 = ROOT.TFile(infile_40)
ntuple_file_45 = ROOT.TFile(infile_45)
ntuple_file_50 = ROOT.TFile(infile_50)

######## LABEL & SAVE WHERE #########

#if len(argv)>4:
 #  saveWhere='~/www/Research/'+argv[5]+'_'
saveWhere='~/www/Research/'+argv[10]+'_'

#####################################
#Get NTUPLE                 #
#####################################


ntuple_10 = ntuple_file_10.Get("tree/Ntuple")
ntuple_15 = ntuple_file_15.Get("tree/Ntuple")
ntuple_20 = ntuple_file_20.Get("tree/Ntuple")
ntuple_25 = ntuple_file_25.Get("tree/Ntuple")
ntuple_30 = ntuple_file_30.Get("tree/Ntuple")
ntuple_35 = ntuple_file_35.Get("tree/Ntuple")
ntuple_40 = ntuple_file_40.Get("tree/Ntuple")
ntuple_45 = ntuple_file_45.Get("tree/Ntuple")
ntuple_50 = ntuple_file_50.Get("tree/Ntuple")

canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)

canvas
ntuple_10.Draw("genPt/cTPGe5x5:TPG5x5_tpgeta>>l10_1(56,0,56,100,0,7)","","BOX")
ntuple_15.Draw("genPt/cTPGe5x5:TPG5x5_tpgeta>>l15_1(56,0,56,100,0,7)","","BOX")
ntuple_20.Draw("genPt/cTPGe5x5:TPG5x5_tpgeta>>l20_1(56,0,56,100,0,7)","","BOX")
ntuple_25.Draw("genPt/cTPGe5x5:TPG5x5_tpgeta>>l25_1(56,0,56,100,0,7)","","BOX")
ntuple_30.Draw("genPt/cTPGe5x5:TPG5x5_tpgeta>>l30_1(56,0,56,100,0,7)","","BOX")
ntuple_35.Draw("genPt/cTPGe5x5:TPG5x5_tpgeta>>l35_1(56,0,56,100,0,7)","","BOX")
ntuple_40.Draw("genPt/cTPGe5x5:TPG5x5_tpgeta>>l40_1(56,0,56,100,0,7)","","BOX")
ntuple_45.Draw("genPt/cTPGe5x5:TPG5x5_tpgeta>>l45_1(56,0,56,100,0,7)","","BOX")
ntuple_50.Draw("genPt/cTPGe5x5:TPG5x5_tpgeta>>l50_1(56,0,56,100,0,7)","","BOX")
l10_1 = ROOT.gDirectory.Get("l10_1")
l15_1 = ROOT.gDirectory.Get("l15_1")
l20_1 = ROOT.gDirectory.Get("l20_1")
l25_1 = ROOT.gDirectory.Get("l25_1")
l30_1 = ROOT.gDirectory.Get("l30_1")
l35_1 = ROOT.gDirectory.Get("l35_1")
l40_1 = ROOT.gDirectory.Get("l40_1")
l45_1 = ROOT.gDirectory.Get("l45_1")
l50_1 = ROOT.gDirectory.Get("l50_1")
l15_1.SetTitle('GenPt/TPG5x5 vs TPG Eta')
profilel10_1 = l10_1.ProfileX("_profilel10_1")
profilel15_1 = l15_1.ProfileX("_profilel15_1")
profilel20_1 = l20_1.ProfileX("_profilel20_1")
profilel25_1 = l25_1.ProfileX("_profilel25_1")
profilel30_1 = l30_1.ProfileX("_profilel30_1")
profilel35_1 = l35_1.ProfileX("_profilel35_1")
profilel40_1 = l40_1.ProfileX("_profilel40_1")
profilel45_1 = l45_1.ProfileX("_profilel45_1")
profilel50_1 = l50_1.ProfileX("_profilel50_1")
hproj10_1 = profilel10_1.ProjectionX()
hproj15_1 = profilel15_1.ProjectionX()
hproj20_1 = profilel20_1.ProjectionX()
hproj25_1 = profilel25_1.ProjectionX()
hproj30_1 = profilel30_1.ProjectionX()
hproj35_1 = profilel35_1.ProjectionX()
hproj40_1 = profilel40_1.ProjectionX()
hproj45_1 = profilel45_1.ProjectionX()
hproj50_1 = profilel50_1.ProjectionX()
hproj10_1.SetLineColor(ROOT.EColor.kBlue+2)
hproj15_1.SetLineColor(ROOT.EColor.kOrange)
hproj20_1.SetLineColor(ROOT.EColor.kGreen-3)
hproj25_1.SetLineColor(ROOT.EColor.kPink-3)
hproj30_1.SetLineColor(ROOT.EColor.kBlue-6)
hproj35_1.SetLineColor(ROOT.EColor.kYellow+3)
hproj40_1.SetLineColor(ROOT.EColor.kAzure+6)
hproj45_1.SetLineColor(ROOT.EColor.kRed-7)
hproj50_1.SetLineColor(ROOT.EColor.kMagenta+2)

hproj10_1.SetMarkerColor(ROOT.EColor.kBlue+2)
hproj15_1.SetMarkerColor(ROOT.EColor.kOrange)
hproj20_1.SetMarkerColor(ROOT.EColor.kGreen-3)
hproj25_1.SetMarkerColor(ROOT.EColor.kPink-3)
hproj30_1.SetMarkerColor(ROOT.EColor.kBlue-6)
hproj35_1.SetMarkerColor(ROOT.EColor.kYellow+3)
hproj40_1.SetMarkerColor(ROOT.EColor.kAzure+6)
hproj45_1.SetMarkerColor(ROOT.EColor.kRed-7)
hproj50_1.SetMarkerColor(ROOT.EColor.kMagenta+2)

hproj15_1.GetYaxis().SetRangeUser(0.7,2.1)
#hproj15_1.GetXaxis().SetRangeUser(6,15)
hproj15_1.GetXaxis().SetTitle("TPG Eta")
hproj15_1.GetYaxis().SetTitle("GenPT/TriggerPt")
hproj10_1.SetMarkerStyle(23)
hproj15_1.SetMarkerStyle(23)
hproj20_1.SetMarkerStyle(23)
hproj25_1.SetMarkerStyle(23)
hproj30_1.SetMarkerStyle(23)
hproj35_1.SetMarkerStyle(23)
hproj40_1.SetMarkerStyle(23)
hproj45_1.SetMarkerStyle(23)
hproj50_1.SetMarkerStyle(23)
hproj10_1.SetLineWidth(2)
hproj15_1.SetLineWidth(2)
hproj20_1.SetLineWidth(2)
hproj25_1.SetLineWidth(2)
hproj30_1.SetLineWidth(2)
hproj35_1.SetLineWidth(2)
hproj40_1.SetLineWidth(2)
hproj45_1.SetLineWidth(2)
hproj50_1.SetLineWidth(2)
hproj15_1.Draw("")
hproj20_1.Draw("same")
hproj25_1.Draw("same")
hproj30_1.Draw("same")
hproj35_1.Draw("same")
hproj40_1.Draw("same")
hproj45_1.Draw("same")
hproj50_1.Draw("same")
hproj10_1.Draw("same")
legend1 = ROOT.TLegend(0.7, 0.72, 0.99, 0.99, "", "brNDC")
legend1.SetFillColor(ROOT.EColor.kWhite)
legend1.SetBorderSize(1)
legend1.AddEntry(hproj10_1, "Pi0 Pt=10 GeV")
legend1.AddEntry(hproj15_1, "Pi0 Pt=15 GeV")
legend1.AddEntry(hproj20_1, "Pi0 Pt=20 GeV")
legend1.AddEntry(hproj25_1, "Pi0 Pt=25 GeV")
legend1.AddEntry(hproj30_1, "Pi0 Pt=30 GeV")
legend1.AddEntry(hproj35_1, "Pi0 Pt=35 GeV")
legend1.AddEntry(hproj40_1, "Pi0 Pt=40 GeV")
legend1.AddEntry(hproj45_1, "Pi0 Pt=45 GeV")
legend1.AddEntry(hproj50_1, "Pi0 Pt=50 GeV")
legend1.Draw("same")
saveas=saveWhere+'SF_eta.png'
canvas.SaveAs(saveas)



#file=ROOT.TFile("outfile.root","RECREATE")
#file.cd()
#hproj15_1.Write()
#hproj10_1.Write()
#hproj20_1.Write()
#hproj25_1.Write()
#hproj30_1.Write()
#hproj35_1.Write()
#hproj40_1.Write()
#hproj45_1.Write()
#hproj50_1.Write()


#for i in range (1,57):
#        SF = hproj10_1.GetBinContent(i)
#        print '%f,' %(SF) 
#for i in range (1,57):
#        SF = hproj15_1.GetBinContent(i)
#        print '%f,' %(SF) 
#for i in range (1,57):
#        SF = hproj20_1.GetBinContent(i)
#        print '%f,' %(SF) 
#for i in range (1,57):
#        SF = hproj25_1.GetBinContent(i)
#        print '%f,' %(SF) 
#for i in range (1,57):
#        SF = hproj30_1.GetBinContent(i)
#        print '%f,' %(SF) 
#for i in range (1,57):
#        SF = hproj35_1.GetBinContent(i)
#        print '%f,' %(SF) 
#for i in range (1,57):
#        SF = hproj40_1.GetBinContent(i)
#        print '%f,' %(SF) 
#for i in range (1,57):
#        SF = hproj45_1.GetBinContent(i)
#        print '%f,' %(SF) 
for i in range (1,57):
        SF = hproj50_1.GetBinContent(i)
        print '%f,' %(SF) 
#

