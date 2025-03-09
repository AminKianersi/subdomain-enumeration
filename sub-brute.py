import argparse
import dns.resolver
from concurrent.futures import ThreadPoolExecutor

print(" ▗▄▖ ▗▖  ▗▖▗▄▄▄▖▗▖  ▗▖▗▖ ▗▖▗▄▄▄▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄▖▗▄▄▖  ▗▄▄▖▗▄▄▄")
print("▐▌ ▐▌▐▛▚▞▜▌  █  ▐▛▚▖▐▌▐▌▗▞▘  █  ▐▌ ▐▌▐▛▚▖▐▌▐▌   ▐▌ ▐▌▐▌     █")
print("▐▛▀▜▌▐▌  ▐▌  █  ▐▌ ▝▜▌▐▛▚▖   █  ▐▛▀▜▌▐▌ ▝▜▌▐▛▀▀▘▐▛▀▚▖ ▝▀▚▖  █") 
print("▐▌ ▐▌▐▌  ▐▌▗▄█▄▖▐▌  ▐▌▐▌ ▐▌▗▄█▄▖▐▌ ▐▌▐▌  ▐▌▐▙▄▄▖▐▌ ▐▌▗▄▄▞▘▗▄█▄▖")
print("================================================================")

print("[Create By Amin Kianersi]")

def load_wordlist(path):
    try:
        with open(path, 'r') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Error: File {path} not found!")
        exit()

def check_subdomain(sub, domain, resolver):
    target = f"{sub}.{domain}"
    try:
        resolver.resolve(target, 'A', lifetime=3)
        return target
    except:
        return None

def subdomain_bruteforce(domain, wordlist, threads=50):
    found = []
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '1.1.1.1']
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(
            lambda sub: check_subdomain(sub, domain, resolver),
            wordlist
        )
    
    for result in results:
        if result:
            print(f"[+] Active: {result}")
            found.append(result)
    
    return found

def save_results(filename, subdomains):
    with open(filename, 'w') as f:
        for sub in subdomains:
            f.write(sub + "\n")

def main():
    parser = argparse.ArgumentParser(description="subdomain brute")
    parser.add_argument('-d', '--domain', required=True, help="Main domain (example: example.com)")
    parser.add_argument('-w', '--wordlist', required=True, help="Wordlist file path")
    parser.add_argument('-o', '--output', default='found_subs.txt', help="Output")
    args = parser.parse_args()

    wordlist = load_wordlist(args.wordlist)
    print(f"[*] Starting scan for {args.domain} with {len(wordlist)} subdomains...")
    
    found = subdomain_bruteforce(args.domain, wordlist)
    
    save_results(args.output, found)
    print(f"\n[+] Completed! {len(found)} active subdomains found.")
    print(f"[+] The results were stored in {args.output}.")

if __name__ == '__main__':
    main()
    

print("========================================")
print("Create By Amin Kianersi (Utred)")
print("========================================")
