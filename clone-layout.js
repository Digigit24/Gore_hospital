/**
 * clone-layout-v3.js - Final version
 * 
 * Corrected section order from reference:
 * HEAD → HEADER → BANNER → ABOUT → SERVICES → TEAM → TESTIMONIALS → WHY-CHOOSE-US → FAQ → FOOTER → MOBILE-MENU → SCRIPTS
 * 
 * Strategy: Take the reference file, replace content-specific sections
 * with cardiology content from the backup files.
 */

const fs = require('fs');
const path = require('path');

const BASE_DIR = __dirname;
const REFERENCE_FILE = path.join(BASE_DIR, 'best-gynecologist-in-akurdi.html');

const TARGET_FILES = [
    { file: 'best-cardiology-hospital-in-akurdi.html', location: 'Akurdi', urlSlug: 'akurdi' },
    { file: 'best-cardiology-hospital-in-mamurdi.html', location: 'Mamurdi', urlSlug: 'mamurdi' },
    { file: 'best-cardiology-hospital-in-nigdi.html', location: 'Nigdi', urlSlug: 'nigdi' },
    { file: 'best-cardiology-hospital-in-pcmc.html', location: 'PCMC', urlSlug: 'pcmc' },
    { file: 'best-cardiology-hospital-in-pradhikaran.html', location: 'Pradhikaran', urlSlug: 'pradhikaran' },
    { file: 'best-cardiology-hospital-in-ravet.html', location: 'Ravet', urlSlug: 'ravet' },
];

function norm(s) { return s.replace(/\r\n/g, '\n').replace(/\r/g, '\n'); }

function main() {
    const refRaw = fs.readFileSync(REFERENCE_FILE, 'utf-8');
    const ref = norm(refRaw);
    console.log(`Reference: ${ref.length} chars`);

    // Find reference section positions
    const refPositions = {
        aboutStart: ref.indexOf('<div class="rts-about-area'),
        serviceStart: ref.indexOf('<div class="service-area'),
        teamStart: ref.indexOf('<div class="team-area-start'),
        testimonialsStart: ref.indexOf('<div class="rts-testimonials-area'),
        whyChooseStart: ref.indexOf('<div class="why-choose-us-area-wrapper'),
        faqCommentStart: ref.indexOf('<!-- FAQ Section'),
        footerStart: ref.indexOf('<div id="footer-placeholder">'),
        mobileMenuStart: ref.indexOf('<!-- mobile menu'),
    };

    console.log('Reference section positions:', refPositions);

    for (const target of TARGET_FILES) {
        const targetPath = path.join(BASE_DIR, target.file);
        const bakPath = targetPath + '.bak';

        console.log(`\n======= ${target.file} =======`);

        // Read from backup (original cardiology file)
        if (!fs.existsSync(bakPath)) {
            console.log('  No backup found, using current file');
            fs.writeFileSync(bakPath, fs.readFileSync(targetPath, 'utf-8'), 'utf-8');
        }
        const srcRaw = fs.readFileSync(bakPath, 'utf-8');
        const src = norm(srcRaw);
        console.log(`  Source: ${src.length} chars, ${src.split('\n').length} lines`);

        // ═══ Extract cardiology content sections ═══

        // 1. Meta tags
        const titleMatch = src.match(/<title>(.*?)<\/title>/s);
        const title = titleMatch ? titleMatch[1].trim() : `Best Cardiology Hospital in ${target.location}`;

        const descMatch = src.match(/<meta\s+name="description"\s+content="([^"]*)"/s);
        const metaDesc = descMatch ? descMatch[1] : '';

        // 2. Banner H1
        const h1Match = src.match(/<h1\s+class="title wow fadeInUp"[^>]*>([\s\S]*?)<\/h1>/);
        const bannerH1 = h1Match ? h1Match[1].trim() : `Best Cardiology Hospital in ${target.location}`;

        // 3. Banner description
        const bannerPMatch = src.match(/<p\s+class="disc wow fadeInUp"[^>]*>([\s\S]*?)<\/p>/);
        const bannerP = bannerPMatch ? bannerPMatch[1].trim() : '';

        // 4. About section: from <div class="rts-about-area to <div class="service-area
        const srcAboutStart = src.indexOf('<div class="rts-about-area');
        const srcServiceStart = src.indexOf('<div class="service-area');
        const aboutSection = (srcAboutStart !== -1 && srcServiceStart !== -1) ?
            src.substring(srcAboutStart, srcServiceStart).trim() : '';

        // 5. Services section: from <div class="service-area to <div class="team-area-start
        // Also includes "Heart Problems We Treat" section (<div class="problem-area)
        const srcTeamStart = src.indexOf('<div class="team-area-start');
        const servicesSection = (srcServiceStart !== -1 && srcTeamStart !== -1) ?
            src.substring(srcServiceStart, srcTeamStart).trim() : '';

        // 6. Team section: from <div class="team-area-start to <div class="amenities-area or testimonials
        // In original cardiology, order is: team → amenities → testimonials → FAQ
        const srcAmenitiesStart = src.indexOf('<div class="amenities-area');
        const srcTestStart = src.indexOf('<div class="rts-testimonials-area');
        // Team ends at whichever comes first: amenities or testimonials
        let srcTeamEnd = srcAmenitiesStart !== -1 ? srcAmenitiesStart : srcTestStart;
        const teamSection = (srcTeamStart !== -1 && srcTeamEnd !== -1) ?
            src.substring(srcTeamStart, srcTeamEnd).trim() : '';

        // 7. Testimonials section: from rts-testimonials-area to FAQ
        const srcFaqText = src.indexOf('Frequently Asked Questions');
        let srcFaqStart = -1;
        if (srcFaqText !== -1) {
            srcFaqStart = src.lastIndexOf('<div class="service-details', srcFaqText);
        }
        const testimonialsSection = (srcTestStart !== -1 && srcFaqStart !== -1) ?
            src.substring(srcTestStart, srcFaqStart).trim() : '';

        // 8. FAQ section: from <div class="service-details (FAQ) to <div id="footer-placeholder">
        const srcFooter = src.indexOf('<div id="footer-placeholder">');
        const faqSection = (srcFaqStart !== -1 && srcFooter !== -1) ?
            src.substring(srcFaqStart, srcFooter).trim() : '';

        console.log(`  Extracted: about=${aboutSection.length} services=${servicesSection.length} team=${teamSection.length} testimonials=${testimonialsSection.length} faq=${faqSection.length}`);

        // ═══ Build output from reference template ═══

        let output = ref;

        // --- Replace meta tags ---
        output = output.replace(/<title>.*?<\/title>/s, `<title>${title}</title>`);
        output = output.replace(/(<meta\s+name="description"\s+content=")[^"]*(")/s, `$1${metaDesc}$2`);
        output = output.replace(/(<link\s+rel="canonical"\s+href=")[^"]*(")/,
            `$1https://gorehospital.com/best-cardiology-hospital-in-${target.urlSlug}.html$2`);

        // OG tags
        output = output.replace(/(<meta\s+property="og:url"\s+content=")[^"]*(")/,
            `$1https://gorehospital.com/best-cardiology-hospital-in-${target.urlSlug}.html$2`);
        output = output.replace(/(<meta\s+property="og:title"\s+content=")[^"]*(")/,
            `$1${title}$2`);
        output = output.replace(/(<meta\s+property="og:description"\s+content=")[^"]*(")/s,
            `$1${metaDesc}$2`);
        output = output.replace(/(<meta\s+property="og:image"\s+content=")[^"]*(")/,
            `$1https://gorehospital.com/assets/logo.jpeg$2`);

        // Twitter tags
        output = output.replace(/(<meta\s+name="twitter:url"\s+content=")[^"]*(")/,
            `$1https://gorehospital.com/best-cardiology-hospital-in-${target.urlSlug}.html$2`);
        output = output.replace(/(<meta\s+name="twitter:title"\s+content=")[^"]*(")/,
            `$1${title}$2`);
        output = output.replace(/(<meta\s+name="twitter:description"\s+content=")[^"]*(")/s,
            `$1${metaDesc}$2`);
        output = output.replace(/(<meta\s+name="twitter:image"\s+content=")[^"]*(")/,
            `$1https://gorehospital.com/assets/logo.jpeg$2`);

        // --- Replace banner H1 ---
        output = output.replace(
            /(<h1\s+class="title wow fadeInUp"[^>]*>)([\s\S]*?)(<\/h1>)/,
            `$1\n                    ${bannerH1}\n                  $3`
        );

        // --- Replace banner description --- 
        output = output.replace(
            /(<p\s+class="disc wow fadeInUp"[^>]*>)([\s\S]*?)(<\/p>)/,
            `$1\n                    ${bannerP}\n                  $3`
        );

        // --- Replace "Trusted by Women" text ---
        output = output.replace(
            /Trusted by Over 10,000\+ Women \| 24\/7 Emergency Care Available \| Cashless Insurance Accepted/,
            'Trusted by Thousands of Heart Patients | 24/7 Emergency Cardiac Care | Cashless Insurance Accepted'
        );

        // Now do the BIG section replacements using the reference positions (recalculated after text replacements)
        // Since text replacements above change positions, we need to find fresh positions

        // --- Replace About section ---
        if (aboutSection) {
            const p1 = output.indexOf('<div class="rts-about-area');
            const p2 = output.indexOf('<div class="service-area');
            if (p1 !== -1 && p2 !== -1) {
                output = output.substring(0, p1) + aboutSection + '\n\n    ' + output.substring(p2);
            }
        }

        // --- Replace Services section ---
        if (servicesSection) {
            const p1 = output.indexOf('<div class="service-area');
            const p2 = output.indexOf('<div class="team-area-start');
            if (p1 !== -1 && p2 !== -1) {
                output = output.substring(0, p1) + servicesSection + '\n\n    ' + output.substring(p2);
            }
        }

        // --- Replace Team section ---
        // In reference: Team is followed by Testimonials
        if (teamSection) {
            const p1 = output.indexOf('<div class="team-area-start');
            const p2 = output.indexOf('<div class="rts-testimonials-area');
            if (p1 !== -1 && p2 !== -1) {
                output = output.substring(0, p1) + teamSection + '\n\n\n    ' + output.substring(p2);
            }
        }

        // --- Replace Testimonials section ---
        // In reference: Testimonials is followed by why-choose-us-area-wrapper
        if (testimonialsSection) {
            const p1 = output.indexOf('<div class="rts-testimonials-area');
            const p2 = output.indexOf('<div class="why-choose-us-area-wrapper');
            if (p1 !== -1 && p2 !== -1) {
                output = output.substring(0, p1) + testimonialsSection + '\n\n\n    ' + output.substring(p2);
            }
        }

        // --- Keep why-choose-us (amenities) from reference --- (hospital-wide)

        // --- Replace FAQ section ---
        // In reference: FAQ has <!-- FAQ Section comment --> then <style> CSS block, then <div class="service-details ...">
        // We keep the comment + CSS from reference, and only replace the content div
        if (faqSection) {
            // Find the <div class="service-details that contains the FAQ in the output
            const faqTextInOutput = output.indexOf('Frequently Asked Questions');
            const refFaqDiv = faqTextInOutput !== -1 ? output.lastIndexOf('<div class="service-details', faqTextInOutput) : -1;
            const footer = output.indexOf('<div id="footer-placeholder">');
            if (refFaqDiv !== -1 && footer !== -1) {
                output = output.substring(0, refFaqDiv) + faqSection + '\n\n    ' + output.substring(footer);
            }
        }

        // --- Keep footer, mobile menu, loader, scripts from reference ---

        // Convert to Windows line endings
        const finalOutput = output.replace(/\n/g, '\r\n');

        fs.writeFileSync(targetPath, finalOutput, 'utf-8');
        console.log(`  Written: ${finalOutput.length} chars, ${finalOutput.split('\r\n').length} lines`);

        // ═══ Verification ═══
        const v = finalOutput;
        const checks = {
            'Title': v.includes(`<title>${title}</title>`),
            'Canonical': v.includes(`best-cardiology-hospital-in-${target.urlSlug}.html`),
            'Mega-menu': v.includes('rts-mega-menu'),
            'Banner H1': v.includes(bannerH1.substring(0, 30)),
            'About section': v.includes('About Gore Multispeciality'),
            'Heart content': v.includes('Heart') || v.includes('heart') || v.includes('cardiol'),
            'Doc cards': v.includes('doc-card'),
            'Why-choose amenities': v.includes('why-choose-us-area-wrapper'),
            'Testimonials': v.includes('rts-testimonials-area') || v.includes('single-testimonials-style'),
            'FAQ': v.includes('Frequently Asked Questions'),
            'FAQ CSS': v.includes('Service Details (Accordion / FAQ)'),
            'Footer': v.includes('footer-placeholder'),
            'Mobile menu': v.includes('mobile-menu-main'),
            'Loader': v.includes('loader-wrapper'),
            'Progress': v.includes('progress-wrap'),
            'Taskade': v.includes('taskade'),
            'Schema': v.includes('application/ld+json'),
            'Analytics': v.includes('gtag'),
            'Doc reorder': v.includes('slidesWithImages'),
            'Form integration': v.includes('form-integration'),
        };

        let failed = 0;
        for (const [name, passed] of Object.entries(checks)) {
            if (!passed) {
                console.log(`  ❌ ${name}`);
                failed++;
            }
        }
        if (failed === 0) {
            console.log('  ✅ All ' + Object.keys(checks).length + ' checks passed!');
        } else {
            console.log(`  ⚠️  ${failed}/${Object.keys(checks).length} checks failed`);
        }
    }

    console.log('\n🎉 Done!');
}

main();
