#!/usr/bin/env bash
echo hello
steps/scoring/score_kaldi_wer.sh "$@"
steps/scoring/score_kaldi_cer.sh --stage 2 "$@"
echo "finished!"