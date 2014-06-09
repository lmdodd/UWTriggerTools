'''
Usage:python jetEfficiencyPlot.py RootFile.root label[optional]

Script to make some quick efficiency plots to test ntuple generation.


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
else:
   saveWhere='~/www/Research/'

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
ntuple_10.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l10_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
ntuple_15.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l15_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
ntuple_20.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l20_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
ntuple_20.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l20_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
ntuple_35.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l35_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
ntuple_50.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l50_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
l15_1 = ROOT.gDirectory.Get("l15_1")
l20_1 = ROOT.gDirectory.Get("l20_1")
l35_1 = ROOT.gDirectory.Get("l35_1")
l50_1 = ROOT.gDirectory.Get("l50_1")
l15_1.SetTitle('GenPt/TriggerPt vs RCT Eta')
profilel15_1 = l15_1.ProfileX("_profilel15_1")
profilel20_1 = l20_1.ProfileX("_profilel20_1")
profilel35_1 = l35_1.ProfileX("_profilel35_1")
profilel50_1 = l50_1.ProfileX("_profilel50_1")
hproj15_1 = profilel15_1.ProjectionX()
hproj20_1 = profilel20_1.ProjectionX()
hproj35_1 = profilel35_1.ProjectionX()
hproj50_1 = profilel50_1.ProjectionX()
hproj15_1.SetLineColor(ROOT.EColor.kCyan)
hproj20_1.SetLineColor(ROOT.EColor.kBlue)
hproj35_1.SetLineColor(ROOT.EColor.kRed)
hproj50_1.SetLineColor(ROOT.EColor.kMagenta)
hproj15_1.GetYaxis().SetRangeUser(0.7,1.2)
hproj15_1.GetXaxis().SetTitle("Region RCT Eta")
hproj15_1.GetYaxis().SetTitle("GenPT/TriggerPt")
hproj15_1.SetMarkerStyle(23)
hproj20_1.SetMarkerStyle(23)
hproj35_1.SetMarkerStyle(23)
hproj50_1.SetMarkerStyle(23)
hproj15_1.SetLineWidth(2)
hproj20_1.SetLineWidth(2)
hproj35_1.SetLineWidth(2)
hproj50_1.SetLineWidth(2)
hproj15_1.Draw("")
hproj20_1.Draw("same")
hproj35_1.Draw("same")
hproj50_1.Draw("same")
legend1 = ROOT.TLegend(0.7, 0.82, 0.99, 0.99, "", "brNDC")
legend1.SetFillColor(ROOT.EColor.kWhite)
legend1.SetBorderSize(1)
legend1.AddEntry(profilel15_2, "Pion0 Pt=10 GeV")
legend1.AddEntry(profilel20_2, "Pion0 Pt=15 GeV")
legend1.AddEntry(profilel35_2, "Pion0 Pt=20 GeV")
legend1.AddEntry(profilel50_2, "Pion0 Pt=25 GeV")
legend1.Draw("same")
saveas=saveWhere+'SF_eta.png'
canvas.SaveAs(saveas)

