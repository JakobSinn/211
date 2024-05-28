import numpy as np
import math
from plotnine import *
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
#ab hier der tatsächliche code
def sinfit(x,a,b,c,w):
    return a*np.sin((x+b)*w)+c
def hfunc(x, a, b, c, w):
    #annahme: keine dämpfung
    return(np.abs(np.sin((x+a)*w)*b)+c)
def fitbesser(zeitarray, signalarray,titleinput):
    #zeitarray, signalarray sind arrays mit der zweit in s und dem ausschlag bei jeder messung
    #titleinput ist ein String, der als titel des Plots und des gespeicherten bilds verwendet wird
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
    #Zur kontrolle: print(zeitarray[peaks])
    abstand = zeitarray[peaks[len(peaks)-1]] - zeitarray[peaks[0]]
    print('Abstand zwischen letzten und ersten peak:',abstand,'s')
    kurzfreq = (len(peaks)-1)/abstand
    print('Schnelles Signal: Frequenz',str(round(kurzfreq,3)),'Hz, Periode:',str(1/kurzfreq))
    popthuelle, pcovhuelle = curve_fit(
        hfunc, zeitarray[peaks], signalarray[peaks],
        p0=[1, 100, 10, 0.2])
    print(popthuelle)
    huellefreq = popthuelle[3]/(2*math.pi)
    print('Frequenz der Einhuellenden',huellefreq,'Periode',(1/huellefreq))
    huelle = hfunc(zeitarray,*popthuelle)
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