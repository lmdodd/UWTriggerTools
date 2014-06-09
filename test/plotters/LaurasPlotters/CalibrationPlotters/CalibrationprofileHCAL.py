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

infile_15 = argv[1]
infile_20 = argv[2]
infile_35 = argv[3]
infile_50 = argv[4]

ntuple_file_15 = ROOT.TFile(infile_15)
ntuple_file_20 = ROOT.TFile(infile_20)
ntuple_file_35 = ROOT.TFile(infile_35)
ntuple_file_50 = ROOT.TFile(infile_50)

######## LABEL & SAVE WHERE #########

if len(argv)>4:
   saveWhere='~/www/Research/'+argv[5]+'_'
else:
   saveWhere='~/www/Research/'

#####################################
#Get NTUPLE                 #
#####################################


ntuple_15 = ntuple_file_15.Get("tree/Ntuple")
ntuple_20 = ntuple_file_20.Get("tree/Ntuple")
ntuple_35 = ntuple_file_35.Get("tree/Ntuple")
ntuple_50 = ntuple_file_50.Get("tree/Ntuple")

canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)

def make_plot(tree, variable, selection, binning, xaxis='', title=''):
    ''' Plot a variable using draw and return the histogram '''
    draw_string = "%s>>htemp(%s)" % (variable, ", ".join(str(x) for x in binning))
    tree.Draw(draw_string, selection, "BOX")
    output_histo = ROOT.gDirectory.Get("htemp").Clone()
    output_histo.GetXaxis().SetTitle(xaxis)
    output_histo.SetTitle(title)
    return output_histo

def profile_ptoffset(ntuple, variable, restrictions, binning, filename,
                         title='', xaxis=''):
    l1g = make_plot(
        ntuple, variable,
        restrictions,
        binning
    )

    frame = ROOT.TH2F("frame", "frame", *binning)
    frame.SetMaximum(30)
    frame.SetTitle(title)
    frame.GetXaxis().SetTitle(xaxis)
    frame.Draw()
    l1g.Draw('BOX')
    profilel1g=l1g.ProfileX(l1g.GetName() + "_profilel1g")
    profilel1g.SetMarkerStyle(23)
    l1g.GetXaxis().SetTitle("Gen Pt")
    l1g.GetYaxis().SetTitle("Gen Pt-Trigger Pt")
    profilel1g.SetLineWidth(2)
    return profilel1g

canvas
ntuple_15.Draw("genPt/maxEg2x1Pt:genRgnEta>>l15_1","maxEg2x1Pt>0 && abs(genEta)<1.479","BOX")
ntuple_20.Draw("genPt/maxEg2x1Pt:genRgnEta>>l20_1","maxEg2x1Pt>0 && abs(genEta)<1.479","BOX")
ntuple_35.Draw("genPt/maxEg2x1Pt:genRgnEta>>l35_1","maxEg2x1Pt>0 && abs(genEta)<1.479","BOX")
ntuple_50.Draw("genPt/maxEg2x1Pt:genRgnEta>>l50_1","maxEg2x1Pt>0 && abs(genEta)<1.479","BOX")
l15_1 = ROOT.gDirectory.Get("l15_1")
l20_1 = ROOT.gDirectory.Get("l20_1")
l35_1 = ROOT.gDirectory.Get("l35_1")
l50_1 = ROOT.gDirectory.Get("l50_1")
l15_1.SetLineColor(ROOT.EColor.kCyan)
l20_1.SetLineColor(ROOT.EColor.kBlue)
l35_1.SetLineColor(ROOT.EColor.kRed)
l50_1.SetLineColor(ROOT.EColor.kMagenta)
l15_1.SetTitle(' genPt/Trigger Pt vs gen GCT Eta')
profilel15_1 = l15_1.ProfileX("_profilel15_1")
profilel20_1 = l20_1.ProfileX("_profilel20_1")
profilel35_1 = l35_1.ProfileX("_profilel35_1")
profilel50_1 = l50_1.ProfileX("_profilel50_1")
profilel15_1.GetYaxis().SetRangeUser(0,3)
profilel15_1.GetXaxis().SetTitle("Gct Eta")
profilel15_1.GetYaxis().SetTitle("L1 GenPT/TriggerPT")
profilel15_1.SetMarkerStyle(23)
profilel20_1.SetMarkerStyle(23)
profilel35_1.SetMarkerStyle(23)
profilel50_1.SetMarkerStyle(23)
profilel15_1.SetLineWidth(2)
profilel20_1.SetLineWidth(2)
profilel35_1.SetLineWidth(2)
profilel50_1.SetLineWidth(2)
profilel15_1.Draw("")
profilel20_1.Draw("same")
profilel35_1.Draw("same")
profilel50_1.Draw("same")
legend1 = ROOT.TLegend(0.7, 0.82, 0.99, 0.99, "", "brNDC")
legend1.SetFillColor(ROOT.EColor.kWhite)
legend1.SetBorderSize(1)
legend1.AddEntry(profilel15_1, "Pion0 Pt=20 GeV")
legend1.AddEntry(profilel20_1, "Pion0 Pt=30 GeV")
legend1.AddEntry(profilel35_1, "Pion0 Pt=40 GeV")
legend1.AddEntry(profilel50_1, "Pion0 Pt=50 GeV")
legend1.Draw("same")
saveas=saveWhere+'SF_eg.png'
canvas.SaveAs(saveas)


canvas
ntuple_15.Draw("genPt/maxRegionPt:genRgnEta>>l15_2","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_20.Draw("genPt/maxRegionPt:genRgnEta>>l20_2","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_35.Draw("genPt/maxRegionPt:genRgnEta>>l35_2","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_50.Draw("genPt/maxRegionPt:genRgnEta>>l50_2","maxRegionPt>0 && abs(genEta)<1.479","BOX")
l15_2 = ROOT.gDirectory.Get("l15_2")
l20_2 = ROOT.gDirectory.Get("l20_2")
l35_2 = ROOT.gDirectory.Get("l35_2")
l50_2 = ROOT.gDirectory.Get("l50_2")
l15_2.SetLineColor(ROOT.EColor.kCyan)
l20_2.SetLineColor(ROOT.EColor.kBlue)
l35_2.SetLineColor(ROOT.EColor.kRed)
l50_2.SetLineColor(ROOT.EColor.kMagenta)
l15_2.SetTitle('genPt/TriggerPt vs gen GCT Eta')
profilel15_2 = l15_2.ProfileX("_profilel15_2")
profilel20_2 = l20_2.ProfileX("_profilel20_2")
profilel35_2 = l35_2.ProfileX("_profilel35_2")
profilel50_2 = l50_2.ProfileX("_profilel50_2")
profilel15_2.GetYaxis().SetRangeUser(0,3)
profilel15_2.GetXaxis().SetTitle("Gct Eta")
profilel15_2.GetYaxis().SetTitle("L1 GenPT/TriggerPT")
profilel15_2.SetMarkerStyle(23)
profilel20_2.SetMarkerStyle(23)
profilel35_2.SetMarkerStyle(23)
profilel50_2.SetMarkerStyle(23)
profilel15_2.SetLineWidth(2)
profilel20_2.SetLineWidth(2)
profilel35_2.SetLineWidth(2)
profilel50_2.SetLineWidth(2)
profilel15_2.Draw("")
profilel20_2.Draw("same")
profilel35_2.Draw("same")
profilel50_2.Draw("same")
legend1.Draw("same")
saveas=saveWhere+'SF_region.png'
canvas.SaveAs(saveas)


canvas
ntuple_15.Draw("(genPt-maxRegionPt)/genPt>>l15_3(50,-.4,1)","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_20.Draw("(genPt-maxRegionPt)/genPt>>l20_3(50,-.4,1)","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_35.Draw("(genPt-maxRegionPt)/genPt>>l35_3(50,-.4,1)","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_50.Draw("(genPt-maxRegionPt)/genPt>>l50_3(50,-.4,1)","maxRegionPt>0 && abs(genEta)<1.479","BOX")
l15_3 = ROOT.gDirectory.Get("l15_3")
l20_3 = ROOT.gDirectory.Get("l20_3")
l35_3 = ROOT.gDirectory.Get("l35_3")
l50_3 = ROOT.gDirectory.Get("l50_3")
l15_3.SetLineColor(ROOT.EColor.kCyan)
l20_3.SetLineColor(ROOT.EColor.kBlue)
l35_3.SetLineColor(ROOT.EColor.kRed)
l50_3.SetLineColor(ROOT.EColor.kMagenta)
l15_3.SetTitle('Resolution: Max Region')
profilel15_3 = l15_3
profilel20_3 = l20_3
profilel35_3 = l35_3
profilel50_3 = l50_3
profilel15_3.GetXaxis().SetTitle("(genPt-TriggerPt)/genPt")
profilel15_3.SetNormFactor(1)
profilel20_3.SetNormFactor(1)
profilel35_3.SetNormFactor(1)
profilel50_3.SetNormFactor(1)
profilel15_3.Rebin()
profilel20_3.Rebin()
profilel35_3.Rebin()
profilel50_3.Rebin()
profilel15_3.SetMarkerStyle(23)
profilel20_3.SetMarkerStyle(23)
profilel35_3.SetMarkerStyle(23)
profilel50_3.SetMarkerStyle(23)
profilel15_3.SetLineWidth(2)
profilel20_3.SetLineWidth(2)
profilel35_3.SetLineWidth(2)
profilel50_3.SetLineWidth(2)
profilel15_3.Draw("")
profilel20_3.Draw("same")
profilel35_3.Draw("same")
profilel50_3.Draw("same")
legend1.Draw("same")
saveas=saveWhere+'resolution_region.png'
canvas.SaveAs(saveas)

canvas
ntuple_15.Draw("(genPt-(maxRegionPt+maxRegionPt_2ndPt))/genPt>>l15_4(50,-.4,1)","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_20.Draw("(genPt-(maxRegionPt+maxRegionPt_2ndPt))/genPt>>l20_4(50,-.4,1)","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_35.Draw("(genPt-(maxRegionPt+maxRegionPt_2ndPt))/genPt>>l35_4(50,-.4,1)","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_50.Draw("(genPt-(maxRegionPt+maxRegionPt_2ndPt))/genPt>>l50_4(50,-.4,1)","maxRegionPt>0 && abs(genEta)<1.479","BOX")
l15_4 = ROOT.gDirectory.Get("l15_4")
l20_4 = ROOT.gDirectory.Get("l20_4")
l35_4 = ROOT.gDirectory.Get("l35_4")
l50_4 = ROOT.gDirectory.Get("l50_4")
l15_4.SetLineColor(ROOT.EColor.kCyan)
l20_4.SetLineColor(ROOT.EColor.kBlue)
l35_4.SetLineColor(ROOT.EColor.kRed)
l50_4.SetLineColor(ROOT.EColor.kMagenta)
l15_4.SetTitle('resolution 4x8')
profilel15_4 = l15_4
profilel20_4 = l20_4
profilel35_4 = l35_4
profilel50_4 = l50_4
profilel15_4.GetXaxis().SetTitle("(genPt-4x8TriggerPT)/genPt")
profilel15_4.SetNormFactor(1)
profilel20_4.SetNormFactor(1)
profilel35_4.SetNormFactor(1)
profilel50_4.SetNormFactor(1)
profilel15_4.Rebin()
profilel20_4.Rebin()
profilel35_4.Rebin()
profilel50_4.Rebin()
profilel15_4.SetMarkerStyle(23)
profilel20_4.SetMarkerStyle(23)
profilel35_4.SetMarkerStyle(23)
profilel50_4.SetMarkerStyle(23)
profilel15_4.SetLineWidth(2)
profilel20_4.SetLineWidth(2)
profilel35_4.SetLineWidth(2)
profilel50_4.SetLineWidth(2)
profilel15_4.Draw("")
profilel20_4.Draw("same")
profilel35_4.Draw("same")
profilel50_4.Draw("same")
legend1.Draw("same")
saveas=saveWhere+'resolution_4x8region.png'
canvas.SaveAs(saveas)



canvas
ntuple_15.Draw("genPt/(maxRegionPt+maxRegionPt_2ndPt):genRgnEta>>l15_5","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_15.Draw("genPt/(maxRegionPt+maxRegionPt_2ndPt):genRgnEta>>l15_5","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_20.Draw("genPt/(maxRegionPt+maxRegionPt_2ndPt):genRgnEta>>l20_5","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_35.Draw("genPt/(maxRegionPt+maxRegionPt_2ndPt):genRgnEta>>l35_5","maxRegionPt>0 && abs(genEta)<1.479","BOX")
ntuple_50.Draw("genPt/(maxRegionPt+maxRegionPt_2ndPt):genRgnEta>>l50_5","maxRegionPt>0 && abs(genEta)<1.479","BOX")
l15_5 = ROOT.gDirectory.Get("l15_5")
l20_5 = ROOT.gDirectory.Get("l20_5")
l35_5 = ROOT.gDirectory.Get("l35_5")
l50_5 = ROOT.gDirectory.Get("l50_5")
l15_5.SetLineColor(ROOT.EColor.kCyan)
l20_5.SetLineColor(ROOT.EColor.kBlue)
l35_5.SetLineColor(ROOT.EColor.kRed)
l50_5.SetLineColor(ROOT.EColor.kMagenta)
l15_5.SetTitle('genPt/TriggerPt(4x8) vs gen GCT Eta')
profilel15_5 = l15_5.ProfileX("_profilel15_5")
profilel20_5 = l20_5.ProfileX("_profilel20_5")
profilel35_5 = l35_5.ProfileX("_profilel35_5")
profilel50_5 = l50_5.ProfileX("_profilel50_5")
profilel15_5.GetYaxis().SetRangeUser(0,3)
profilel15_5.GetXaxis().SetTitle("Gct Eta")
profilel15_5.GetYaxis().SetTitle("L1 GenPT/TriggerPT")
profilel15_5.SetMarkerStyle(23)
profilel20_5.SetMarkerStyle(23)
profilel35_5.SetMarkerStyle(23)
profilel50_5.SetMarkerStyle(23)
profilel15_5.SetLineWidth(2)
profilel20_5.SetLineWidth(2)
profilel35_5.SetLineWidth(2)
profilel50_5.SetLineWidth(2)
profilel15_5.Draw("")
profilel20_5.Draw("same")
profilel35_5.Draw("same")
profilel50_5.Draw("same")
legend1.Draw("same")
saveas=saveWhere+'SF_4x8region.png'
canvas.SaveAs(saveas)


canvas
ntuple_15.Draw("(genPt-maxEg2x1Pt)/genPt:genRgnEta>>l15_6","maxEg2x1Pt>0 && abs(genEta)<1.479","BOX")
ntuple_20.Draw("(genPt-maxEg2x1Pt)/genPt:genRgnEta>>l20_6","maxEg2x1Pt>0 && abs(genEta)<1.479","BOX")
ntuple_35.Draw("(genPt-maxEg2x1Pt)/genPt:genRgnEta>>l35_6","maxEg2x1Pt>0 && abs(genEta)<1.479","BOX")
ntuple_50.Draw("(genPt-maxEg2x1Pt)/genPt:genRgnEta>>l50_6","maxEg2x1Pt>0 && abs(genEta)<1.479","BOX")
l15_6 = ROOT.gDirectory.Get("l15_6")
l20_6 = ROOT.gDirectory.Get("l20_6")
l35_6 = ROOT.gDirectory.Get("l35_6")
l50_6 = ROOT.gDirectory.Get("l50_6")
l15_6.SetLineColor(ROOT.EColor.kCyan)
l20_6.SetLineColor(ROOT.EColor.kBlue)
l35_6.SetLineColor(ROOT.EColor.kRed)
l50_6.SetLineColor(ROOT.EColor.kMagenta)
l15_6.SetTitle('genPt/TriggerPt(2x1) vs gen GCT Eta')
profilel15_6 = l15_6.ProfileX("_profilel15_6")
profilel20_6 = l20_6.ProfileX("_profilel20_6")
profilel35_6 = l35_6.ProfileX("_profilel35_6")
profilel50_6 = l50_6.ProfileX("_profilel50_6")
profilel15_6.GetYaxis().SetRangeUser(-0.5,1)
profilel15_6.GetXaxis().SetTitle("Gct Eta")
profilel15_6.GetYaxis().SetTitle("L1 resolution")
profilel15_6.SetMarkerStyle(23)
profilel20_6.SetMarkerStyle(23)
profilel35_6.SetMarkerStyle(23)
profilel50_6.SetMarkerStyle(23)
profilel15_6.SetLineWidth(2)
profilel20_6.SetLineWidth(2)
profilel35_6.SetLineWidth(2)
profilel50_6.SetLineWidth(2)
profilel15_6.Draw("")
profilel20_6.Draw("same")
profilel35_6.Draw("same")
profilel50_6.Draw("same")
legend1.Draw("same")
saveas=saveWhere+'eg_resolution_vseta.png'
canvas.SaveAs(saveas)


