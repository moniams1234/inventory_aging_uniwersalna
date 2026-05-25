/* =========================
   NUMBER INPUT +/- BUTTONS
========================= */

div[data-baseweb="input"] button {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    opacity: 1 !important;
}

div[data-baseweb="input"] button:hover {
    color: #FF4B4B !important;
    background: rgba(255,255,255,0.08) !important;
}

/* =========================
   CUSTOM BUCKET NUMBERS
========================= */

.custom-bucket-index,
.bucket-number,
div[class*="bucket"] span {
    color: #FFFFFF !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
}

/* czerwony akcent dla # */
.custom-bucket-index::first-letter,
.bucket-number::first-letter {
    color: #FF4B4B !important;
}

/* =========================
   RANGE LABELS
========================= */

.custom-bucket-help {
    color: #CBD5E1 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
