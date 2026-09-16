import ROOT, numpy as np
ROOT.gROOT.SetBatch(True)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
m=ROOT.RooRealVar("m_yy","m",105,160,"GeV"); m.setBins(55)
a0=ROOT.RooRealVar("a0","",-0.02,-0.5,0.2); e=ROOT.RooExponential("e","",m,a0)
n=ROOT.RooRealVar("n","",300.,0,5000)
ext=ROOT.RooAddPdf("ext","",ROOT.RooArgList(e),ROOT.RooArgList(n))
a1=ext.generateBinned(ROOT.RooArgSet(m), ROOT.RooFit.ExpectedData(True)); a1.SetName("a1")
a2=ext.generateBinned(ROOT.RooArgSet(m), ROOT.RooFit.ExpectedData(True)); a2.SetName("a2")
cat=ROOT.RooCategory("cat","cat"); cat.defineType("c1"); cat.defineType("c2")
sim=ROOT.RooSimultaneous("sim","",cat); sim.addPdf(ext,"c1"); sim.addPdf(ext,"c2")
print("Import-style combined:")
try:
    comb=ROOT.RooDataHist("comb","comb",ROOT.RooArgList(m),ROOT.RooFit.Index(cat),
                          ROOT.RooFit.Import("c1",a1),ROOT.RooFit.Import("c2",a2))
    print(" ok",comb.numEntries(),comb.sumEntries())
except Exception as ex: print(" FAIL",ex)
w=ROOT.RooWorkspace("w","w")
getattr(w,"import")(sim, ROOT.RooFit.RecycleConflictNodes())
try:
    getattr(w,"import")(comb); print(" comb imported")
except Exception as ex: print(" comb import FAIL",ex)
w.writeToFile("/tmp/w2.root"); print("ws ok")
try:
    t=ROOT.RooJSONFactoryWSTool(w); t.exportJSON("/tmp/w2.json"); print("HS3 ok")
except Exception as ex: print("HS3 FAIL", type(ex).__name__, str(ex)[:300])
