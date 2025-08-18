const dns = require('dns').promises;

/**
 * Perform comprehensive DNS lookup for an email address or domain
 * @param {string} input - Email address or domain to lookup
 */
async function performDNSLookup(input) {
    // Determine if input is email or domain
    let domain, email;
    if (input.includes('@')) {
        email = input;
        domain = input.split('@')[1];
    } else {
        domain = input;
        email = `example@${domain}`;
    }
    
    console.log(`\n🔍 DNS Lookup for: ${input}`);
    console.log(`📧 Domain: ${domain}`);
    console.log('=' .repeat(50));
    
    try {
        // MX Records - Mail Exchange
        console.log('\n📬 MX Records (Mail Exchange):');
        try {
            const mxRecords = await dns.resolveMx(domain);
            mxRecords.forEach((record, index) => {
                console.log(`  ${index + 1}. Priority: ${record.priority}, Exchange: ${record.exchange}`);
            });
        } catch (error) {
            console.log(`  ❌ Error: ${error.message}`);
        }

        // A Records - IPv4 addresses
        console.log('\n🌐 A Records (IPv4):');
        try {
            const aRecords = await dns.resolve4(domain);
            aRecords.forEach((record, index) => {
                console.log(`  ${index + 1}. ${record}`);
            });
        } catch (error) {
            console.log(`  ❌ Error: ${error.message}`);
        }

        // AAAA Records - IPv6 addresses
        console.log('\n🌐 AAAA Records (IPv6):');
        try {
            const aaaaRecords = await dns.resolve6(domain);
            aaaaRecords.forEach((record, index) => {
                console.log(`  ${index + 1}. ${record}`);
            });
        } catch (error) {
            console.log(`  ❌ Error: ${error.message}`);
        }

        // SPF Records - Sender Policy Framework
        console.log('\n🛡️  SPF Records (Sender Policy Framework):');
        try {
            const txtRecords = await dns.resolveTxt(domain);
            const spfRecords = txtRecords.filter(record => 
                record.some(txt => txt.startsWith('v=spf1'))
            );
            
            if (spfRecords.length > 0) {
                spfRecords.forEach((record, index) => {
                    console.log(`  ${index + 1}. ${record.join('')}`);
                });
            } else {
                console.log('  ❌ No SPF records found');
            }
        } catch (error) {
            console.log(`  ❌ Error: ${error.message}`);
        }

        // DMARC Records
        console.log('\n🔒 DMARC Records:');
        try {
            const dmarcDomain = `_dmarc.${domain}`;
            const dmarcRecords = await dns.resolveTxt(dmarcDomain);
            const validDmarc = dmarcRecords.filter(record => 
                record.some(txt => txt.startsWith('v=DMARC1'))
            );
            
            if (validDmarc.length > 0) {
                validDmarc.forEach((record, index) => {
                    console.log(`  ${index + 1}. ${record.join('')}`);
                });
            } else {
                console.log('  ❌ No DMARC records found');
            }
        } catch (error) {
            console.log(`  ❌ Error: ${error.message}`);
        }

        // DKIM Records (common selectors)
        console.log('\n🔑 DKIM Records (Common Selectors):');
        const commonSelectors = ['default', 'selector1', 'selector2', 'google', 'k1', 's1', 's2'];
        
        for (const selector of commonSelectors) {
            try {
                const dkimDomain = `${selector}._domainkey.${domain}`;
                const dkimRecords = await dns.resolveTxt(dkimDomain);
                const validDkim = dkimRecords.filter(record => 
                    record.some(txt => txt.includes('k=rsa') || txt.includes('v=DKIM1'))
                );
                
                if (validDkim.length > 0) {
                    console.log(`  ✅ ${selector}: Found DKIM record`);
                    validDkim.forEach(record => {
                        const dkimText = record.join('');
                        console.log(`     ${dkimText.substring(0, 100)}${dkimText.length > 100 ? '...' : ''}`);
                    });
                }
            } catch (error) {
                // Silently continue - most selectors won't exist
            }
        }

        // NS Records - Name Servers
        console.log('\n🌍 NS Records (Name Servers):');
        try {
            const nsRecords = await dns.resolveNs(domain);
            nsRecords.forEach((record, index) => {
                console.log(`  ${index + 1}. ${record}`);
            });
        } catch (error) {
            console.log(`  ❌ Error: ${error.message}`);
        }

        // TXT Records - All text records
        console.log('\n📝 All TXT Records:');
        try {
            const txtRecords = await dns.resolveTxt(domain);
            txtRecords.forEach((record, index) => {
                const txtContent = record.join('');
                console.log(`  ${index + 1}. ${txtContent}`);
            });
        } catch (error) {
            console.log(`  ❌ Error: ${error.message}`);
        }

        console.log('\n' + '=' .repeat(50));
        console.log('✅ DNS lookup completed successfully');

    } catch (error) {
        console.error(`❌ General DNS lookup error: ${error.message}`);
    }
}

// Main execution
async function main() {
    // Get command line arguments
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log('❌ Error: Please provide an email address or domain');
        console.log('\n📖 Usage:');
        console.log('  node dns-lookup.js <email@domain.com>');
        console.log('  node dns-lookup.js <domain.com>');
        console.log('\n📝 Examples:');
        console.log('  node dns-lookup.js ammar.khalid@onespherelabs.com.au');
        console.log('  node dns-lookup.js google.com');
        console.log('  node dns-lookup.js user@example.org');
        process.exit(1);
    }
    
    const input = args[0];
    
    // Basic validation
    if (input.includes('@')) {
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(input)) {
            console.log('❌ Error: Invalid email format');
            console.log('   Expected format: user@domain.com');
            process.exit(1);
        }
    } else {
        // Domain validation
        const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?\.([a-zA-Z]{2,}\.?)+$/;
        if (!domainRegex.test(input)) {
            console.log('❌ Error: Invalid domain format');
            console.log('   Expected format: domain.com');
            process.exit(1);
        }
    }
    
    console.log('🚀 Starting DNS Lookup Tool');
    console.log(`⏰ Timestamp: ${new Date().toISOString()}`);
    console.log(`🎯 Target: ${input}`);
    
    await performDNSLookup(input);
    
    console.log('\n🏁 DNS lookup tool finished');
}

// Run the script
if (require.main === module) {
    main().catch(console.error);
}

module.exports = { performDNSLookup };
