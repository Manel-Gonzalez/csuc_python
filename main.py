from requests import get, exceptions
from concurrent.futures import ThreadPoolExecutor
import time

TXT_LIST = False
TIMEOUT = 5


def print_if_active(domain):
    """ Si el domini està actiu (no aixeca cap excepció relacionada amb la inactivitat),
        imprimeix el domini per pantalla."""
    try:
        get(f'http://{domain}', timeout=TIMEOUT)
    except (exceptions.ConnectionError, exceptions.ReadTimeout) as e:
        pass
    else:
        print(domain)


def print_active_domains(fileName):
    """ Llegeix els dominis d'un fitxer txt (cada domini és una línia) i crida la funció
        print if active sobre cada un d'ells."""
    with open(fileName, 'r') as f:
        for domain in f.readlines():
            clean_domain = domain.rstrip("\n")
            print_if_active(clean_domain)


if __name__ == '__main__':

    if (TXT_LIST):
        # En cas que s'hagi de llegir d'un fitxer txt.
        # No he vist la manera de fer que l'execució de lectura sigui paral·lela, i triga bastant si
        # el fitxer conté molts dominis, depenent del timeout escollit
        start_time = time.time()
        print_active_domains('domains.txt')
        print("--- %s seconds ---" % (time.time() - start_time))

    else:
        # En el cas que tinguem la llista en memòria, es poden processar de manera paral·lela els dominis.
        # Exemple de dominis
        domains = ["aaa.com", "cvdefvdffdvvdfdvfdfv.com", "aarp.com", "abarth.com", "abb.com", "abbott.com", "abbvie.com",
                   "abc.com", "able.com", "abogado.com", "abudhabi.com", "ac.com", "acdemy.com", "accenture.com", "accountant.com",
                   "accountants.com", "aco.com", "actor.com", "ad.com", "adac.com", "ads.com", "adult.com", "ae.com",
                   "aeg.com", "aero.com", "aetna.com", "af.com", "afamilycompany.com", "afl.com", "africa.com"]
        start_time = time.time()
        with ThreadPoolExecutor() as executor:
            executor.map(print_if_active, domains)
        print("--- %s seconds ---" % (time.time() - start_time))
