#!/usr/bin/env bash
# Simulated Antigravity session for the demo GIF.
# Pacing tuned for readability — not a real antigravity invocation.

set -u

BOLD=$'\033[1m'
DIM=$'\033[2m'
CYAN=$'\033[36m'
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
GRAY=$'\033[90m'
RESET=$'\033[0m'

p() { printf "%b\n" "$1"; }
slow() { sleep "${1:-0.4}"; }
type_line() {
  # Print $1 char-by-char to simulate typing.
  local line="$1"
  local delay="${2:-0.012}"
  for ((i=0; i<${#line}; i++)); do
    printf "%s" "${line:$i:1}"
    sleep "$delay"
  done
  printf "\n"
}

clear
p "${GRAY}~/pti-claim-agent \$${RESET} ${BOLD}antigravity${RESET}"
slow 0.8
p "${DIM}Starting Antigravity... reading ANTIGRAVITY.md${RESET}"
slow 1.0
p ""
p "${CYAN}●${RESET} ${DIM}Ready. Drop receipts in chat and tell me who to file for.${RESET}"
slow 1.2
p ""
p "${GRAY}You:${RESET}"
slow 0.3
type_line "file a claim for my father" 0.025
p "${GRAY}     📎 invoice.pdf  📎 IMG_0001.HEIC  📎 IMG_0002.HEIC${RESET}"
slow 1.3
p ""
p "${CYAN}●${RESET} Reading 3 files..."
slow 0.7
p "${CYAN}●${RESET} Converting HEIC → JPEG (sips)..."
slow 0.6
p "${CYAN}●${RESET} Extracting claim details..."
slow 1.2
p ""
p "${BOLD}Claim summary${RESET}"
p "  Insured       ${BOLD}Nguyễn Văn A${RESET}          ${GRAY}(father)${RESET}"
p "  Hospital      Example Clinic — HCMC"
p "  Date          25/05/2026"
p "  Diagnosis     Dental — fillings, extraction, scaling, CT"
p "  Amount        ${BOLD}3,100,000 VND${RESET}        ${GRAY}(private dental, no BHYT)${RESET}"
slow 1.5
p ""
p "Confirm? ${BOLD}y/n${RESET}"
slow 0.9
p "${GRAY}You:${RESET} ${BOLD}y${RESET}"
slow 0.8
p ""
p "${CYAN}●${RESET} Filling blank_form.docx with policy + insured + bank..."
slow 0.7
p "${CYAN}●${RESET} Embedding signature into form..."
slow 0.6
p "${CYAN}●${RESET} Bundling form + evidence → ${BOLD}output/NguyenVanA_2026-05-25/${RESET}"
slow 0.6
p "${CYAN}●${RESET} Creating Gmail draft with 4 attachments..."
slow 1.0
p ""
p "${GREEN}✓ Draft created.${RESET}"
p "  ${DIM}Subject:${RESET} HS YCBT - Nguyen Van A - 0000XXX/.../MAR01"
p "  ${DIM}TO:${RESET}      claims@insurer.example"
p "  ${DIM}CC:${RESET}      broker@example.com, you@example.com"
p "  ${DIM}Attached:${RESET} GYC_NguyenVanA_25-05-2026.docx, invoice.pdf,"
p "             treatment_record.jpg, payment_receipt.jpg"
slow 1.5
p ""
p "${YELLOW}→ Review in Gmail and send.${RESET}"
slow 2.0
