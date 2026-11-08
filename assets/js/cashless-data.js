/*
 * ==========================================================================
 *  CASHLESS FACILITY - SINGLE SOURCE OF TRUTH
 *  (insurance companies + TPAs shown on the home page and on
 *   /cashless-facility.html)
 * ==========================================================================
 *
 *  How to update the insurer list
 *  ------------------------------
 *  1. Edit the PARTNERS array below - one line per company:
 *       { name: "Full Company Name", logo: "/assets/logos/insurers/slug.png", type: "insurer" },
 *     - type is "insurer" or "tpa"
 *     - display order = order in this file
 *     - add a company  -> add a line
 *     - remove one     -> delete its line
 *     - no logo yet    -> leave the path pointing at the expected file (or set logo: "");
 *                         the tile shows the company initials until the file exists.
 *  2. Regenerate the HTML (needs Node.js, run from the repo root):
 *       node scripts/build-cashless.js
 *     This rewrites the markup between <!-- cashless:start --> and
 *     <!-- cashless:end --> in index.html and cashless-facility.html.
 *     Never hand-edit the markup between those markers.
 *  3. Commit index.html, cashless-facility.html and this file together.
 *
 *  Logos only (no data change)
 *  ---------------------------
 *  Drop the image into assets/logos/insurers/ or assets/logos/tpas/ using the
 *  exact filename referenced below. NO rebuild is needed - the HTML already
 *  points at that path. PNG/WebP/SVG, ~400px wide, transparent or white
 *  background. To use a different extension, change the path here and rebuild.
 *
 *  This file is read by the build script only; it is not loaded by the website.
 * ==========================================================================
 */

const NOTE =
  "Before admission, please confirm once with the Mediclaim Department about the Cashless Facility.";

// Shown next to the note as a tel: link. Currently the hospital's main line.
const MEDICLAIM_PHONE = { label: "Mediclaim Department", display: "+91 96895 28414", tel: "+919689528414" };

const PARTNERS = [
  // ---- Empanelled Insurance Companies --------------------------------------
  { name: "Acko General Insurance Limited", logo: "/assets/logos/insurers/acko.png", type: "insurer" },
  { name: "Bajaj Allianz General Insurance Company Limited", logo: "/assets/logos/insurers/bajaj-allianz.png", type: "insurer" },
  { name: "Star Health and Allied Insurance Co. Ltd.", logo: "/assets/logos/insurers/star-health.png", type: "insurer" },
  { name: "Cholamandalam MS General Insurance Co. Ltd.", logo: "/assets/logos/insurers/cholamandalam-ms.png", type: "insurer" },
  { name: "HDFC ERGO General Insurance Company Limited", logo: "/assets/logos/insurers/hdfc-ergo.png", type: "insurer" },
  { name: "Aditya Birla Health Insurance Co. Ltd.", logo: "/assets/logos/insurers/aditya-birla-health.png", type: "insurer" },
  { name: "ICICI Lombard General Insurance Co. Ltd.", logo: "/assets/logos/insurers/icici-lombard.png", type: "insurer" },
  { name: "TATA AIG General Insurance Co. Ltd.", logo: "/assets/logos/insurers/tata-aig.png", type: "insurer" },
  { name: "National Insurance Co. Ltd.", logo: "/assets/logos/insurers/national-insurance.png", type: "insurer" },
  { name: "United India Insurance Co. Ltd.", logo: "/assets/logos/insurers/united-india.png", type: "insurer" },
  { name: "The Oriental Insurance Company Limited", logo: "/assets/logos/insurers/oriental-insurance.png", type: "insurer" },
  { name: "The New India Assurance Company Limited", logo: "/assets/logos/insurers/new-india-assurance.png", type: "insurer" },
  { name: "Niva Bupa Health Insurance Co. Ltd.", logo: "/assets/logos/insurers/niva-bupa.png", type: "insurer" },
  { name: "Navi General Insurance Co. Ltd.", logo: "/assets/logos/insurers/navi-general.png", type: "insurer" },
  { name: "SBI General Insurance Co. Ltd.", logo: "/assets/logos/insurers/sbi-general.png", type: "insurer" },
  { name: "Go Digit General Insurance Limited", logo: "/assets/logos/insurers/go-digit.png", type: "insurer" },
  { name: "Future Generali India Insurance Co. Ltd.", logo: "/assets/logos/insurers/future-generali.png", type: "insurer" },
  { name: "IFFCO Tokio General Insurance Co. Ltd.", logo: "/assets/logos/insurers/iffco-tokio.png", type: "insurer" },
  { name: "Reliance General Insurance Co. Ltd.", logo: "/assets/logos/insurers/reliance-general.png", type: "insurer" },
  { name: "Care Health Insurance Co. Ltd.", logo: "/assets/logos/insurers/care-health.png", type: "insurer" },
  { name: "Royal Sundaram General Insurance Co. Ltd.", logo: "/assets/logos/insurers/royal-sundaram.png", type: "insurer" },
  { name: "Universal Sompo General Insurance Co. Ltd.", logo: "/assets/logos/insurers/universal-sompo.png", type: "insurer" },
  { name: "ManipalCigna Health Insurance Co. Ltd.", logo: "/assets/logos/insurers/manipalcigna.png", type: "insurer" },
  { name: "Kshema General Insurance Company Limited", logo: "/assets/logos/insurers/kshema-general.png", type: "insurer" },
  { name: "Liberty General Insurance Limited", logo: "/assets/logos/insurers/liberty-general.png", type: "insurer" },
  { name: "Magma HDI General Insurance Limited", logo: "/assets/logos/insurers/magma-hdi.png", type: "insurer" },
  { name: "Raheja QBE General Insurance Co. Ltd.", logo: "/assets/logos/insurers/raheja-qbe.png", type: "insurer" },
  { name: "Shriram General Insurance Co. Ltd.", logo: "/assets/logos/insurers/shriram-general.png", type: "insurer" },
  { name: "Zuno General Insurance Limited", logo: "/assets/logos/insurers/zuno-general.png", type: "insurer" },
  { name: "Zurich Kotak General Insurance Company Limited", logo: "/assets/logos/insurers/zurich-kotak.png", type: "insurer" },
  { name: "Narayana Health Insurance Limited", logo: "/assets/logos/insurers/narayana-health.png", type: "insurer" },
  { name: "Galaxy Health Insurance Company Limited", logo: "/assets/logos/insurers/galaxy-health.png", type: "insurer" },
  { name: "NVGT Care Services Pvt. Ltd.", logo: "/assets/logos/insurers/nvgt-care.png", type: "insurer" },

  // ---- Empanelled TPAs -----------------------------------------------------
  { name: "Medi Assist India TPA Pvt. Ltd.", logo: "/assets/logos/tpas/medi-assist.png", type: "tpa" },
  { name: "MD India Health Care Services (TPA) Pvt. Ltd.", logo: "/assets/logos/tpas/md-india.png", type: "tpa" },
  { name: "Paramount Health Services (TPA) Pvt. Ltd.", logo: "/assets/logos/tpas/paramount-health.png", type: "tpa" },
  { name: "Family Health Plan Insurance TPA Ltd.", logo: "/assets/logos/tpas/family-health-plan.png", type: "tpa" },
  { name: "Health India Service TPA Pvt. Ltd.", logo: "/assets/logos/tpas/health-india.png", type: "tpa" },
  { name: "Heritage Health TPA Pvt. Ltd.", logo: "/assets/logos/tpas/heritage-health.png", type: "tpa" },
  { name: "Health Insurance TPA of India Ltd.", logo: "/assets/logos/tpas/health-insurance-tpa-of-india.png", type: "tpa" },
  { name: "Good Health Plan Ltd.", logo: "/assets/logos/tpas/good-health-plan.png", type: "tpa" },
  { name: "Vidal Health TPA Pvt. Ltd.", logo: "/assets/logos/tpas/vidal-health.png", type: "tpa" },
];

module.exports = { NOTE, MEDICLAIM_PHONE, PARTNERS };
