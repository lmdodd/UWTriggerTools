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
ntuple_10.Draw("TPGe5x5>>l10_1(40,0,80)","","BOX")
ntuple_15.Draw("TPGe5x5>>l15_1(40,0,80)","","BOX")
ntuple_20.Draw("TPGe5x5>>l20_1(40,0,80)","","BOX")
ntuple_25.Draw("TPGe5x5>>l25_1(40,0,80)","","BOX")
ntuple_30.Draw("TPGe5x5>>l30_1(40,0,80)","","BOX")
ntuple_35.Draw("TPGe5x5>>l35_1(40,0,80)","","BOX")
ntuple_40.Draw("TPGe5x5>>l40_1(40,0,80)","","BOX")
ntuple_45.Draw("TPGe5x5>>l45_1(40,0,80)","","BOX")
ntuple_50.Draw("TPGe5x5>>l50_1(40,0,80)","","BOX")
l10_1 = ROOT.gDirectory.Get("l10_1")
l15_1 = ROOT.gDirectory.Get("l15_1")
l20_1 = ROOT.gDirectory.Get("l20_1")
l25_1 = ROOT.gDirectory.Get("l25_1")
l30_1 = ROOT.gDirectory.Get("l30_1")
l35_1 = ROOT.gDirectory.Get("l35_1")
l40_1 = ROOT.gDirectory.Get("l40_1")
l45_1 = ROOT.gDirectory.Get("l45_1")
l50_1 = ROOT.gDirectory.Get("l50_1")
l10_1.SetLineColor(ROOT.EColor.kBlue+2)
l15_1.SetLineColor(ROOT.EColor.kOrange)
l20_1.SetLineColor(ROOT.EColor.kGreen-3)
l25_1.SetLineColor(ROOT.EColor.kPink-3)
l30_1.SetLineColor(ROOT.EColor.kBlue-6)
l35_1.SetLineColor(ROOT.EColor.kYellow+3)
l40_1.SetLineColor(ROOT.EColor.kAzure+6)
l45_1.SetLineColor(ROOT.EColor.kRed-7)
l50_1.SetLineColor(ROOT.EColor.kMagenta+2)
l15_1.GetXaxis().SetTitle("TPGe5x5")
l10_1.SetMarkerStyle(23)
l15_1.SetMarkerStyle(23)
l20_1.SetMarkerStyle(23)
l25_1.SetMarkerStyle(23)
l30_1.SetMarkerStyle(23)
l35_1.SetMarkerStyle(23)
l40_1.SetMarkerStyle(23)
l45_1.SetMarkerStyle(23)
l50_1.SetMarkerStyle(23)
l10_1.SetLineWidth(2)
l15_1.SetLineWidth(2)
l20_1.SetLineWidth(2)
l25_1.SetLineWidth(2)
l30_1.SetLineWidth(2)
l35_1.SetLineWidth(2)
l40_1.SetLineWidth(2)
l45_1.SetLineWidth(2)
l50_1.SetLineWidth(2)
l15_1.Draw("")
l10_1.Draw("same")
l20_1.Draw("same")
l25_1.Draw("same")
l30_1.Draw("same")
l35_1.Draw("same")
l40_1.Draw("same")
l45_1.Draw("same")
l50_1.Draw("same")
legend1 = ROOT.TLegend(0.7, 0.72, 0.99, 0.99, "", "brNDC")
legend1.SetFillColor(ROOT.EColor.kWhite)
legend1.SetBorderSize(1)
legend1.AddEntry(l10_1, "Pion0 Pt=10 GeV")
legend1.AddEntry(l15_1, "Pion0 Pt=15 GeV")
legend1.AddEntry(l20_1, "Pion0 Pt=20 GeV")
legend1.AddEntry(l25_1, "Pion0 Pt=25 GeV")
legend1.AddEntry(l30_1, "Pion0 Pt=30 GeV")
legend1.AddEntry(l35_1, "Pion0 Pt=35 GeV")
legend1.AddEntry(l40_1, "Pion0 Pt=40 GeV")
legend1.AddEntry(l45_1, "Pion0 Pt=45 GeV")
legend1.AddEntry(l50_1, "Pion0 Pt=50 GeV")
legend1.Draw("same")
saveas=saveWhere+'TPG_E.png'
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


#print 'pt: 10'
#for i in range (1,23):
#        SF = hproj10_1.GetBinContent(i)
#        print 'eta: %d SF: %f' %(i,SF) 
#print 'pt: 15'
#for i in range (1,23):
#        SF = hproj15_1.GetBinContent(i)
#        print 'eta: %d SF: %f' %(i,SF) 
#print 'pt: 20'
#for i in range (1,23):
#        SF = hproj20_1.GetBinContent(i)
#        print 'eta: %d SF: %f' %(i,SF) 
#print 'pt: 25'
#for i in range (1,23):
#        SF = hproj25_1.GetBinContent(i)
#        print 'eta: %d SF: %f' %(i,SF) 
#print 'pt: 30'
#for i in range (1,23):
#        SF = hproj30_1.GetBinContent(i)
#        print 'eta: %d SF: %f' %(i,SF) 
#print 'pt: 35'
#for i in range (1,23):
#        SF = hproj35_1.GetBinContent(i)
#        print 'eta: %d SF: %f' %(i,SF) 
#print 'pt: 40'
#for i in range (1,23):
#        SF = hproj40_1.GetBinContent(i)
#        print 'eta: %d SF: %f' %(i,SF) 
#print 'pt: 45'
#for i in range (1,23):
#        SF = hproj45_1.GetBinContent(i)
#        print 'eta: %d SF: %f' %(i,SF) 
#print 'pt: 50'
#for i in range (1,23):
#        SF = hproj50_1.GetBinContent(i)
#        print 'eta: %d SF: %f' %(i,SF) 
#

