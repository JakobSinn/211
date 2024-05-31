def sinfit(x,a,b,c,w):
    return a*np.sin((x+b)*w)+c
def hfunc(x, a, b, c, w):
    #annahme: keine dämpfung
    return(np.abs(np.sin((x+a)*w)*b)+c)
def fitbesser(zeitarray, signalarray,titleinput):
    #HINWEIS: Es kann sein, dass p0 (=angegebene geratene Werte für den Fit der Einhuellenden) angepasst werden müssen
    #insbesondere der letzte wert (geratene huellenfrequenz in rad/s)
    dauer = max(zeitarray)
    maxhz = 5 #maximale frequenz des pendels, hier geschätzt
    messpunkte = len(zeitarray)
    messpunktefreq = int(messpunkte/dauer)
    signalbreite = max(signalarray) - min(signalarray)
    signalnull = max(signalarray) - 0.5*signalbreite
    print('Messung mit',messpunktefreq,'Messpunkten pro Sekunde')
    print('Dauer des Signals:',dauer,'s')
    peaks = np.array(
        find_peaks(
            signalarray, 
            distance=(messpunktefreq/maxhz),
            prominence=10)[0])
    print(len(peaks),'peaks im Signal detektiert')
    abstand = zeitarray[peaks[len(peaks)-1]] - zeitarray[peaks[0]]
    #print('Abstand zwischen letzten und ersten peak:',abstand,'s')
    #kurzfreq = (len(peaks)-1)/abstand
    #print('Schnelles Signal: Frequenz',str(round(kurzfreq,3)),'Hz, Periode:',str(1/kurzfreq))
    popthuelle, pcovhuelle = curve_fit(
        hfunc, zeitarray[peaks], signalarray[peaks],
        p0=[2, 100, 10, 0.05])
    popthuelle
    huellefreq = round(np.abs(popthuelle[3])/(2*math.pi),3)
    print('Frequenz der Einhuellenden',huellefreq,'Hz,',str(round(popthuelle[3],3)),'rad/s, Periode',(1/huellefreq))
    huelle = hfunc(zeitarray,*popthuelle)
    huellerel = huelle / (max(huelle)-min(huelle)) #wie nah ist die huelle hier an ihrem peak im vergleich zu den wert, den sie an knoten annimmt?
    peaksimbauch = []
    for peak in peaks:
        #peaks, wo die huelle die hälfte ihre maximalen auslenkung hat, werden mitgenommen
        if huellerel[peak] > 0.7: peaksimbauch.append(zeitarray[peak])
    #differenzen zwischen diesen peaks
    diffpeaksimbauch = np.array(peaksimbauch)[1:] - np.array(peaksimbauch)[:-1]
    #manche der differenzen sind sehr groß, da hier zwischen den paks die knoten liegen
    diffpeaksimbauchclean = [x for x in diffpeaksimbauch if x <= 1.8*np.median(diffpeaksimbauch)]
    kurzperiode = np.mean(diffpeaksimbauchclean)
    kurzfreq = 1/kurzperiode
    print('Schnelles Signal: Frequenz',str(round(kurzfreq,3)),'Hz,', str(round(kurzperiode*2*math.pi,3)), 'rad/s, Periode:',str(kurzperiode))
    showhuelleplus = sinfit(zeitarray, signalbreite/2, popthuelle[0],signalnull,popthuelle[3])
    showhuelleminus = -sinfit(zeitarray, signalbreite/2, popthuelle[0],-signalnull,popthuelle[3])
    #plotten
    plot = (
        ggplot(aes(x=zeitarray))
        + geom_line(aes(y=signalarray))
        + geom_point(aes(x=zeitarray[peaks], y=signalarray[peaks]), color='red')
        + geom_line(aes(y=huelle),linetype='dashed', color='red')
        + geom_hline(yintercept=signalnull, linetype='dashed', color='gray')
        + geom_line(aes(y=showhuelleplus), linetype='dashed')
        + geom_line(aes(y=showhuelleminus), linetype='dashed')
        + labs(
            title=titleinput,
            subtitle='Frequenz Einhüllende: '+str(round(huellefreq,6))+'Hz\nFrequenz Pendel:'+str(round(kurzfreq,5))+'Hz',
            x='Zeit in der Messung [s]',
            y='Auslenkung des Pendels [b.E.]'
        )
    )
    plot.show()
    plot.save(titleinput+'.png', dpi=200)
