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
ntuple_15.Draw("maxRegionPt:maxRegionPt_Eta>>l15_2","maxRegionPt>0","BOX")
ntuple_20.Draw("maxRegionPt:maxRegionPt_Eta>>l20_2","maxRegionPt>0","BOX")
ntuple_35.Draw("maxRegionPt:maxRegionPt_Eta>>l35_2","maxRegionPt>0","BOX")
ntuple_50.Draw("maxRegionPt:maxRegionPt_Eta>>l50_2","maxRegionPt>0","BOX")
l15_2 = ROOT.gDirectory.Get("l15_2")
l20_2 = ROOT.gDirectory.Get("l20_2")
l35_2 = ROOT.gDirectory.Get("l35_2")
l50_2 = ROOT.gDirectory.Get("l50_2")
l15_2.SetLineColor(ROOT.EColor.kCyan)
l20_2.SetLineColor(ROOT.EColor.kBlue)
l35_2.SetLineColor(ROOT.EColor.kRed)
l50_2.SetLineColor(ROOT.EColor.kMagenta)
l15_2.SetTitle('genPt/TriggerPt vs RCT Eta')
profilel15_2 = l15_2.ProfileX("_profilel15_2")
hproj15_2 = profilel15_2.ProjectionX()
profilel20_2 = l20_2.ProfileX("_profilel20_2")
hproj20_2 = profilel20_2.ProjectionX()
profilel35_2 = l35_2.ProfileX("_profilel35_2")
hproj35_2 = profilel35_2.ProjectionX()
profilel50_2 = l50_2.ProfileX("_profilel50_2")
hproj50_2 = profilel50_2.ProjectionX()
profilel15_2.GetYaxis().SetRangeUser(0.6,1.6)
profilel15_2.GetXaxis().SetTitle("Region RCT Eta")
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
legend1 = ROOT.TLegend(0.7, 0.82, 0.99, 0.99, "", "brNDC")
legend1.SetFillColor(ROOT.EColor.kWhite)
legend1.SetBorderSize(1)
legend1.AddEntry(profilel15_2, "Pion0 Pt=15 GeV")
legend1.AddEntry(profilel20_2, "Pion0 Pt=25 GeV")
legend1.AddEntry(profilel35_2, "Pion0 Pt=35 GeV")
legend1.AddEntry(profilel50_2, "Pion0 Pt=45 GeV")
legend1.Draw("same")
saveas=saveWhere+'SF_region.png'
canvas.SaveAs(saveas)


canvas
ntuple_15.Draw("genPt/maxRegionPt:maxRegionPt_Eta>>l15_1(22,0,22,100,0,7)","maxRegionPt>0","BOX")
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
hproj15_1.GetYaxis().SetRangeUser(0.7,2.9)
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
legend1.Draw("same")
saveas=saveWhere+'SF_eta.png'
canvas.SaveAs(saveas)




canvas
ntuple_15.Draw("(genPt-maxRegionPt)/genPt>>l15_3(21,-.4,1)","maxRegionPt>0","BOX")
ntuple_20.Draw("(genPt-maxRegionPt)/genPt>>l20_3(21,-.4,1)","maxRegionPt>0","BOX")
ntuple_35.Draw("(genPt-maxRegionPt)/genPt>>l35_3(21,-.4,1)","maxRegionPt>0","BOX")
ntuple_50.Draw("(genPt-maxRegionPt)/genPt>>l50_3(21,-.4,1)","maxRegionPt>0","BOX")
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
#profilel15_3.SetNormFactor(1)
#profilel20_3.SetNormFactor(1)
#profilel35_3.SetNormFactor(1)
#profilel50_3.SetNormFactor(1)
#profilel15_3.Rebin()
#profilel20_3.Rebin()
#profilel35_3.Rebin()
#profilel50_3.Rebin()
profilel15_3.SetMarkerStyle(23)
profilel20_3.SetMarkerStyle(23)
profilel35_3.SetMarkerStyle(23)
profilel50_3.SetMarkerStyle(23)
profilel15_3.SetLineWidth(2)
profilel20_3.SetLineWidth(2)
profilel35_3.SetLineWidth(2)
profilel50_3.SetLineWidth(2)
#profilel15_3.GetYaxis().SetRangeUser(0,0.39)
profilel15_3.Draw("")
profilel20_3.Draw("same")
profilel35_3.Draw("same")
profilel50_3.Draw("same")
legend1.Draw("same")
saveas=saveWhere+'resolution_region.png'
canvas.SaveAs(saveas)


canvas
ntuple_15.Draw("maxRegionPt-genPt>>l15_9(80,-20,20)","maxRegionPt>0","BOX")
ntuple_20.Draw("maxRegionPt-genPt>>l20_9(80,-20,20)","maxRegionPt>0","BOX")
ntuple_35.Draw("maxRegionPt-genPt>>l35_9(80,-20,20)","maxRegionPt>0","BOX")
ntuple_50.Draw("maxRegionPt-genPt>>l50_9(80,-20,20)","maxRegionPt>0","BOX")
l15_9 = ROOT.gDirectory.Get("l15_9")
l20_9 = ROOT.gDirectory.Get("l20_9")
l35_9 = ROOT.gDirectory.Get("l35_9")
l50_9 = ROOT.gDirectory.Get("l50_9")
l15_9.SetLineColor(ROOT.EColor.kCyan)
l20_9.SetLineColor(ROOT.EColor.kBlue)
l35_9.SetLineColor(ROOT.EColor.kRed)
l50_9.SetLineColor(ROOT.EColor.kMagenta)
l15_9.SetTitle('region Pt-genPt')
profilel15_9 = l15_9
profilel20_9 = l20_9
profilel35_9 = l35_9
profilel50_9 = l50_9
profilel15_9.GetXaxis().SetTitle("RegionPt-GenPt")
profilel15_9.SetNormFactor(1)
profilel20_9.SetNormFactor(1)
profilel35_9.SetNormFactor(1)
profilel50_9.SetNormFactor(1)
profilel15_9.Rebin()
profilel20_9.Rebin()
profilel35_9.Rebin()
profilel50_9.Rebin()
profilel15_9.SetMarkerStyle(23)
profilel20_9.SetMarkerStyle(23)
profilel35_9.SetMarkerStyle(23)
profilel50_9.SetMarkerStyle(23)
profilel15_9.SetLineWidth(2)
profilel20_9.SetLineWidth(2)
profilel35_9.SetLineWidth(2)
profilel50_9.SetLineWidth(2)
profilel15_9.Draw("")
profilel20_9.Draw("same")
profilel35_9.Draw("same")
profilel50_9.Draw("same")
legend1.Draw("same")
saveas=saveWhere+'regiondelta.png'
canvas.SaveAs(saveas)



canvas
ntuple_15.Draw("maxRegionPt>>l15_4(100,0,100)","maxRegionPt>0","BOX")
ntuple_20.Draw("maxRegionPt>>l20_4(100,0,100)","maxRegionPt>0","BOX")
ntuple_35.Draw("maxRegionPt>>l35_4(100,0,100)","maxRegionPt>0","BOX")
ntuple_50.Draw("maxRegionPt>>l50_4(100,0,100)","maxRegionPt>0","BOX")
l15_4 = ROOT.gDirectory.Get("l15_4")
l20_4 = ROOT.gDirectory.Get("l20_4")
l35_4 = ROOT.gDirectory.Get("l35_4")
l50_4 = ROOT.gDirectory.Get("l50_4")
l15_4.SetLineColor(ROOT.EColor.kCyan)
l20_4.SetLineColor(ROOT.EColor.kBlue)
l35_4.SetLineColor(ROOT.EColor.kRed)
l50_4.SetLineColor(ROOT.EColor.kMagenta)
l15_4.SetTitle('region Pt')
profilel15_4 = l15_4
profilel20_4 = l20_4
profilel35_4 = l35_4
profilel50_4 = l50_4
profilel15_4.GetXaxis().SetTitle("RegionPt")
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
saveas=saveWhere+'regionpt.png'
canvas.SaveAs(saveas)



canvas
ntuple_15.Draw("genPt/(maxRegionPt+maxRegionPt_2ndPt):maxRegionPt_Eta>>l15_5","maxRegionPt>0","BOX")
ntuple_15.Draw("genPt/(maxRegionPt+maxRegionPt_2ndPt):maxRegionPt_Eta>>l15_5","maxRegionPt>0","BOX")
ntuple_20.Draw("genPt/(maxRegionPt+maxRegionPt_2ndPt):maxRegionPt_Eta>>l20_5","maxRegionPt>0","BOX")
ntuple_35.Draw("genPt/(maxRegionPt+maxRegionPt_2ndPt):maxRegionPt_Eta>>l35_5","maxRegionPt>0","BOX")
ntuple_50.Draw("genPt/(maxRegionPt+maxRegionPt_2ndPt):maxRegionPt_Eta>>l50_5","maxRegionPt>0","BOX")
l15_5 = ROOT.gDirectory.Get("l15_5")
l20_5 = ROOT.gDirectory.Get("l20_5")
l35_5 = ROOT.gDirectory.Get("l35_5")
l50_5 = ROOT.gDirectory.Get("l50_5")
l15_5.SetLineColor(ROOT.EColor.kCyan)
l20_5.SetLineColor(ROOT.EColor.kBlue)
l35_5.SetLineColor(ROOT.EColor.kRed)
l50_5.SetLineColor(ROOT.EColor.kMagenta)
l15_5.SetTitle('genPt/TriggerPt(4x8) vs region GCT Eta')
profilel15_5 = l15_5.ProfileX("_profilel15_5")
profilel20_5 = l20_5.ProfileX("_profilel20_5")
profilel35_5 = l35_5.ProfileX("_profilel35_5")
profilel50_5 = l50_5.ProfileX("_profilel50_5")
profilel15_5.GetYaxis().SetRangeUser(0.6,1.6)
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
ntuple_15.Draw("(genPt-maxEg2x1Pt)/genPt:maxRegionPt_Eta>>l15_6","maxEg2x1Pt>0 && maxRegionPt>0","BOX")
ntuple_20.Draw("(genPt-maxEg2x1Pt)/genPt:maxRegionPt_Eta>>l20_6","maxEg2x1Pt>0 && maxRegionPt>0","BOX")
ntuple_35.Draw("(genPt-maxEg2x1Pt)/genPt:maxRegionPt_Eta>>l35_6","maxEg2x1Pt>0 && maxRegionPt>0","BOX")
ntuple_50.Draw("(genPt-maxEg2x1Pt)/genPt:maxRegionPt_Eta>>l50_6","maxEg2x1Pt>0 && maxRegionPt>0","BOX")
l15_6 = ROOT.gDirectory.Get("l15_6")
l20_6 = ROOT.gDirectory.Get("l20_6")
l35_6 = ROOT.gDirectory.Get("l35_6")
l50_6 = ROOT.gDirectory.Get("l50_6")
l15_6.SetLineColor(ROOT.EColor.kCyan)
l20_6.SetLineColor(ROOT.EColor.kBlue)
l35_6.SetLineColor(ROOT.EColor.kRed)
l50_6.SetLineColor(ROOT.EColor.kMagenta)
l15_6.SetTitle('eg resolution vs region GCT Eta')
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



canvas
ntuple_15.Draw("(genPt-maxRegionPt)/genPt:maxRegionPt_Eta>>l15_7","maxRegionPt>0","BOX")
ntuple_20.Draw("(genPt-maxRegionPt)/genPt:maxRegionPt_Eta>>l20_7","maxRegionPt>0","BOX")
ntuple_35.Draw("(genPt-maxRegionPt)/genPt:maxRegionPt_Eta>>l35_7","maxRegionPt>0","BOX")
ntuple_50.Draw("(genPt-maxRegionPt)/genPt:maxRegionPt_Eta>>l50_7","maxRegionPt>0","BOX")
l15_7 = ROOT.gDirectory.Get("l15_7")
l20_7 = ROOT.gDirectory.Get("l20_7")
l35_7 = ROOT.gDirectory.Get("l35_7")
l50_7 = ROOT.gDirectory.Get("l50_7")
l15_7.SetLineColor(ROOT.EColor.kCyan)
l20_7.SetLineColor(ROOT.EColor.kBlue)
l35_7.SetLineColor(ROOT.EColor.kRed)
l50_7.SetLineColor(ROOT.EColor.kMagenta)
l15_7.SetTitle('region resolution vs region GCT Eta')
profilel15_7 = l15_7.ProfileX("_profilel15_7")
profilel20_7 = l20_7.ProfileX("_profilel20_7")
profilel35_7 = l35_7.ProfileX("_profilel35_7")
profilel50_7 = l50_7.ProfileX("_profilel50_7")
profilel15_7.GetYaxis().SetRangeUser(-0.5,1)
profilel15_7.GetXaxis().SetTitle("Gct Eta")
profilel15_7.GetYaxis().SetTitle("L1 resolution")
profilel15_7.SetMarkerStyle(23)
profilel20_7.SetMarkerStyle(23)
profilel35_7.SetMarkerStyle(23)
profilel50_7.SetMarkerStyle(23)
profilel15_7.SetLineWidth(2)
profilel20_7.SetLineWidth(2)
profilel35_7.SetLineWidth(2)
profilel50_7.SetLineWidth(2)
profilel15_7.Draw("")
profilel20_7.Draw("same")
profilel35_7.Draw("same")
profilel50_7.Draw("same")
legend1.Draw("same")
saveas=saveWhere+'region_resolution_vseta.png'
canvas.SaveAs(saveas)



