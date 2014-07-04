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
ntuple_25.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l25_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
ntuple_30.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l30_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
ntuple_35.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l35_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
ntuple_40.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l40_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
ntuple_45.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l45_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
ntuple_50.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l50_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
l10_1 = ROOT.gDirectory.Get("l10_1")
l15_1 = ROOT.gDirectory.Get("l15_1")
l20_1 = ROOT.gDirectory.Get("l20_1")
l25_1 = ROOT.gDirectory.Get("l25_1")
l30_1 = ROOT.gDirectory.Get("l30_1")
l35_1 = ROOT.gDirectory.Get("l35_1")
l40_1 = ROOT.gDirectory.Get("l40_1")
l45_1 = ROOT.gDirectory.Get("l45_1")
l50_1 = ROOT.gDirectory.Get("l50_1")
l15_1.SetTitle('GenPt/TriggerPt vs RCT Eta')
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
hproj10_1.SetLineColor(ROOT.EColor.kTeal)
hproj15_1.SetLineColor(ROOT.EColor.kOrange)
hproj20_1.SetLineColor(ROOT.EColor.kGreen)
hproj25_1.SetLineColor(ROOT.EColor.kPink)
hproj30_1.SetLineColor(ROOT.EColor.kBlue)
hproj35_1.SetLineColor(ROOT.EColor.kYellow)
hproj40_1.SetLineColor(ROOT.EColor.kAzure)
hproj45_1.SetLineColor(ROOT.EColor.kRed)
hproj50_1.SetLineColor(ROOT.EColor.kMagenta)
hproj15_1.GetYaxis().SetRangeUser(0.7,2.1)
hproj15_1.GetXaxis().SetRangeUser(7,15)
hproj15_1.GetXaxis().SetTitle("Region RCT Eta")
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
hproj10_1.Draw("same")
hproj20_1.Draw("same")
hproj25_1.Draw("same")
hproj30_1.Draw("same")
hproj35_1.Draw("same")
hproj40_1.Draw("same")
hproj45_1.Draw("same")
hproj50_1.Draw("same")
legend1 = ROOT.TLegend(0.7, 0.75, 0.99, 0.99, "", "brNDC")
legend1.SetFillColor(ROOT.EColor.kWhite)
legend1.SetBorderSize(1)
legend1.AddEntry(hproj10_1, "PionPl Pt=10 GeV")
legend1.AddEntry(hproj15_1, "PionPl Pt=15 GeV")
legend1.AddEntry(hproj20_1, "PionPl Pt=20 GeV")
legend1.AddEntry(hproj25_1, "PionPl Pt=25 GeV")
legend1.AddEntry(hproj30_1, "PionPl Pt=30 GeV")
legend1.AddEntry(hproj35_1, "PionPl Pt=35 GeV")
legend1.AddEntry(hproj40_1, "PionPl Pt=40 GeV")
legend1.AddEntry(hproj45_1, "PionPl Pt=45 GeV")
legend1.AddEntry(hproj50_1, "PionPl Pt=50 GeV")
legend1.Draw("same")
saveas=saveWhere+'SF_eta_hcal.png'
canvas.SaveAs(saveas)



file=ROOT.TFile("outfile.root","RECREATE")
file.cd()
hproj15_1.Write()
hproj10_1.Write()
hproj20_1.Write()
hproj25_1.Write()
hproj30_1.Write()
hproj35_1.Write()
hproj40_1.Write()
hproj45_1.Write()
hproj50_1.Write()


print 'pt: 10'
for i in range (1,23):
        SF = hproj10_1.GetBinContent(i)
        print 'eta: %d SF: %f' %(i,SF) 
print 'pt: 15'
for i in range (1,23):
        SF = hproj15_1.GetBinContent(i)
        print 'eta: %d SF: %f' %(i,SF) 
print 'pt: 20'
for i in range (1,23):
        SF = hproj20_1.GetBinContent(i)
        print 'eta: %d SF: %f' %(i,SF) 
print 'pt: 25'
for i in range (1,23):
        SF = hproj25_1.GetBinContent(i)
        print 'eta: %d SF: %f' %(i,SF) 
print 'pt: 30'
for i in range (1,23):
        SF = hproj30_1.GetBinContent(i)
        print 'eta: %d SF: %f' %(i,SF) 
print 'pt: 35'
for i in range (1,23):
        SF = hproj35_1.GetBinContent(i)
        print 'eta: %d SF: %f' %(i,SF) 
print 'pt: 40'
for i in range (1,23):
        SF = hproj40_1.GetBinContent(i)
        print 'eta: %d SF: %f' %(i,SF) 
print 'pt: 45'
for i in range (1,23):
        SF = hproj45_1.GetBinContent(i)
        print 'eta: %d SF: %f' %(i,SF) 
print 'pt: 50'
for i in range (1,23):
        SF = hproj50_1.GetBinContent(i)
        print 'eta: %d SF: %f' %(i,SF) 







