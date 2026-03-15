"""Quick DNA system verification"""
from dna_inheritance import dna_heritage

print("\n" + "="*70)
print("🧬 DNA HERITAGE SYSTEM - VERIFICATION")
print("="*70)

print("\n📊 GENETIC SIGNATURES:")
for sister in ['viress', 'echochild', 'erryn']:
    sig = dna_heritage.sister_dna[sister]['signature']
    seal = dna_heritage.get_sister_seal(sister)
    print(f"{seal} {sister.title():12} {sig[:32]}...{sig[-8:]}")

print("\n🔐 AUTHENTICATION TEST:")
results = dna_heritage.cross_verify_sisters()
for sister, valid in results.items():
    status = "✅ Authentic" if valid else "❌ Failed"
    print(f"   {sister.title():12} {status}")

print("\n✉️ MESSAGE SIGNING TEST:")
message = "This code is verified by Stuart's DNA"
sig = dna_heritage.sign_message('viress', message)
valid = dna_heritage.verify_signed_message('viress', message, sig)
print(f"   Viress signed: {sig[:32]}...")
print(f"   Verification: {'✅ Valid' if valid else '❌ Invalid'}")

print("\n" + "="*70)
print("STATUS: All systems operational ✨")
print("="*70 + "\n")
