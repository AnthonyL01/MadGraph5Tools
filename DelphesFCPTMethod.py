import ROOT
import sys
import collections 

#============Functions================#

#================ Extracting Data from Delphes root =====================#
def RootReading ( directory, TreeName , Branch, LeafName ):
	LeafValues = []
	File = ROOT.TChain(str(TreeName))
	File.Add(directory)
	Number = File.GetEntries()
	for i in range(Number):
		Entry = File.GetEntry(i)
		string = str("File."+Branch+".GetEntries()")
		EntryFromBranch = eval(string)
		for j in range(EntryFromBranch):
			LeafValue = File.GetLeaf(str(LeafName)).GetValue(j)
			LeafValues.append(LeafValue)
	return LeafValues
#===============End RootReading===================#
			
#======Extracting Data from Delphes Tree==========#
def TreeLeaves ( directory, TreeName, LeafName):
	LeafValues = []
	File = ROOT.TFile(directory)
	string = str("File."+TreeName)
	TreeEvents = eval(string)
	for i in TreeEvents:
		LeafString = str("i."+LeafName)
		Leaf = eval(LeafString)
		LeafValues.append(Leaf)
	return LeafValues
#===========End Delphes Tree =====================#

#============HistoJet ==============================#
def HistoJet ( label, Process, MissingET, SaveHistROOT,scaling ):
	f = ROOT.TFile.Open(SaveHistROOT,"UPDATE")
	StringOfName = "h" + Process +"Nom_" + label + "_obs_met"
	max_size = 200
	min_size = 0
	delta = 20
	lengthy = len(MissingET)
	h1 = ROOT.TH1F(StringOfName,StringOfName,delta,min_size,max_size)
	for i in range(lengthy):
		temp = MissingET[i]
		h1.Fill(temp)
	h1.Scale(scaling)
	h1.Write()
	f.Close()
#=============End HistoJet ===============================#

############Program Start##########################

#============Future Input agruments===============#
directory= str(sys.argv[1])
DelphFile = sys.argv[4]
name = sys.argv[2]
process = sys.argv[3]
output = sys.argv[5]
SaveHistROOT = str(output+"/"+DelphFile)

#===========End Future Input arguments============#
print(SaveHistROOT)
NewFile = ROOT.TFile(SaveHistROOT, "RECREATE")
NewFile.Close()
TreeNames="Delphes"

for i in range(1):
	
	#preparing all the data arrays from Delphes
	ET = RootReading(directory, TreeNames, "MissingET", "MissingET.MET")

	#=====Electrons============# 
	Electron_size = TreeLeaves(directory, TreeNames, "Electron_size")
	ElectronPT = RootReading(directory, TreeNames, "Electron", "Electron.PT")
	ElectronCharge = RootReading(directory, TreeNames, "Electron", "Electron.Charge")
	ElectronEta = RootReading(directory,TreeNames, "Electron", "Electron.Eta")

	#=========Muon=============#
	Muon_size = TreeLeaves(directory, TreeNames, "Muon_size")
	MuonPT = RootReading(directory, TreeNames, "Muon", "Muon.PT")
	MuonCharge = RootReading(directory, TreeNames, "Muon","Muon.Charge")
	MuonEta = RootReading(directory, TreeNames, "Muon", "Muon.Eta")

	#=========Jets=============#
	Jets_size = TreeLeaves(directory, TreeNames, "Jet_size")
	JetPT = RootReading(directory, TreeNames, "Jet", "Jet.PT")
	JetEta = RootReading(directory, TreeNames, "Jet", "Jet.Eta")
	
	#temp iteration variables to retrieve root entries
	EvID = 1
	el = 0
	mu = 0
	je = 0
	
	#Arrays for temporary storing of the entries:
	Electron = []
	Muon = []
	Jet = []
	Jet0 = []	

	#sorting the data into arrays and indexing them with EvID (EventID)
	for i in range(len(Jets_size)):
		JetS = Jets_size[i]
		MuonS = Muon_size[i]
		ElectronS = Electron_size[i]
		MissingET = ET[i]
		
		#Getting entries from leaves of root file
		#==========Electrons=============#
		for e in range(ElectronS):
			EPT = ElectronPT[el]
			ECh = ElectronCharge[el]
			EEta = abs(ElectronEta[el])
			tempE = [EvID, MissingET, EPT, ECh, EEta]
			Electron.append(tempE)
			el = el +1 

		#===========Muon=================#
		for m in range(MuonS):
			MPT = MuonPT[mu]
			MCh = MuonCharge[mu]
			MEta = abs(MuonEta[mu])
			tempM = [EvID, MissingET, MPT, MCh, MEta]
			Muon.append(tempM)
			mu = mu +1

		#============Jets================#
		for j in range(JetS):
			JPT = JetPT[je]
			JEta = abs(JetEta[je])
			tempJ = [EvID, MissingET, JPT, JEta, JetS]
			Jet.append(tempJ)
			je = je +1
		
		if (JetS == 0):
			tempJ0 = [EvID,MissingET,JetS]
			Jet0.append(tempJ0)
		EvID = EvID + 1
	print("Finished reading")
	#Performing the cuts on the arrays: 
	ECutPT = 25
	ECutEta = 2.47
	MCutPT = 20
	MCutEta = 2.5
	JCutPT = 30
	JCutEta = 2.5
	
	#Some arrays for the data satisfying the cuts	
	PassedElectron = []
	PassedMuon = []
	PassedJet = set()
	RejectedJet = []
	
	for e in range(len(Electron)):
		EventID = Electron[e][0]
		MissingET = Electron[e][1]
		EPT = Electron[e][2]
		ECh = Electron[e][3]
		EEta = Electron[e][4]
		if (EPT > ECutPT and EEta < ECutEta):
			passE = [EventID,MissingET,EPT,ECh,EEta]
			PassedElectron.append(passE)

	for m in range(len(Muon)):
		EventID = Muon[m][0]
		MissingET = Muon[e][1]
		MPT = Muon[m][2]
		MCh = Muon[m][3]
		MEta = Muon[m][4]
		if (MPT > MCutPT and MEta < MCutEta):
			passM = [EventID,MissingET,MPT,MCh,MEta]
			PassedMuon.append(passM)

	for j in range(len(Jet)):
		EventID = Jet[j][0]
		JPT = Jet[j][2]
		JEta = Jet[j][3]
		NumberJet = Jet[j][4]
		if (JPT > JCutPT and JEta < JCutEta):
			PassedJet.add(EventID)
		else:
			Reject = [EventID,MissingET,NumberJet]
			RejectedJet.append(Reject)
	
	print("Finished Cutting")
	#Comparing the lepton arrays and enforcing opposite charge 
	#this then leads to opposite charge and opposite flavor
	OpFlOpCh = []
	for e in range(len(PassedElectron)):
		ECharge = PassedElectron[e][3]
		EEvent = PassedElectron[e][0]
		EET = PassedElectron[e][1]
		for m in range(len(PassedMuon)):
			MCharge = PassedMuon[m][3]
			MEvent = PassedMuon[m][0]
			if (ECharge != MCharge and EEvent == MEvent):
				temp = [EEvent,EET]
				OpFlOpCh.append(temp)
	
	#========================jet stuff================================#
	#Compressing the Jet Data into number of jets per run
	#This redefines the number of jets for a given event 
	#since some have been cut out. The first "for" loop 
	#searches the rejected for canditates which can go into J0
	unique = set()
	for rej in range(len(RejectedJet)):
		EventID = RejectedJet[rej][0]
		En = RejectedJet[rej][1]
		NumberJets = RejectedJet[rej][2]
		x = 0 #Counter
		for r in range(len(RejectedJet)):
			Event = RejectedJet[r][0]
			if (Event == EventID):
				x = x +1
				if (x == NumberJets):
					unique.add(EventID)

	#Recovery of ET
	unique = list(unique) #convert from set object to list 	
	for u in range(len(unique)):
		ID = unique[u]
		EID = 1	
		for ev in range(len(ET)):
			Energy = ET[ev]
			if (EID == ID):
				temp = [ID,Energy,0]
				Jet0.append(temp)
			EID = EID +1

	#We Recover the ET again for Jets
	Jets = list(PassedJet)
	Jet = []
	for ID in Jets:
		EID = 1
		for Energy in ET:
			if (EID == ID):
				temps = [ID,Energy]
				Jet.append(temps)
			EID = EID +1
	print("ET Recovery")
	#===================================================================#
	#now compare events in both Jets and OpFlOpCh to find the events which
	#are responsible for the dilepton events 
	Jets = []
	for dl in range(len(OpFlOpCh)):
		EventIDL = OpFlOpCh[dl][0]
		MissingET = OpFlOpCh[dl][1]
		if ( MissingET >= 200 ):
			MissingET = 200
		for j in range(len(Jet)):
			EventIDJ = Jet[j][0]
			if (EventIDL == EventIDJ):
				temp = [EventIDL,MissingET]
				Jets.append(temp)
	
	#Now perform last for loops and only find ET for Jets0 and Jets but before that, check
	#for overlapping events if they are present
	
	I = 0
	for x in range(len(Jet0)):
		Id = Jet0[x][0]
		D = 0
		for j in range(len(Jets)):
			idj = Jets[j][0]
			if (Id == idj):
				Jets.insert(D,[])
				print("removed an entry due to double up check line 265 of Delphes...Method")
				Jet0.insert(I,[])
			D = D +1
		I = I +1
	
	JetET = []
	Jet0ET = []
	for e in range(len(Jets)):
		ET = Jets[e][1]
		if (ET > 200):
			ET = 200
		JetET.append(ET)
	for x in range(len(Jet0)):
		ET0 = Jet0[e][1]
		if (ET > 200):
			ET = 200
		Jet0ET.append(ET0)
	print("Placing new Data in .root")
	HistoJet ( "jets", process,JetET, SaveHistROOT,1 )
	HistoJet ( "jets0", process, Jet0ET, SaveHistROOT,1 )