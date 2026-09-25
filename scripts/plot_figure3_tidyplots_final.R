#!/usr/bin/env Rscript
# Figure 3 formal tidyplots redesign: exercise dynamics.
# Panels: a) 13-contrast NAMPT_z forest; b) immediate/24 h balance trajectory;
# c) 13 contrasts x 4 metrics heatmap. Values are existing audited results.

suppressPackageStartupMessages({
  library(tidyplots)
  library(patchwork)
  library(readr)
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(ragg)
  library(svglite)
})

root <- normalizePath(getwd(), winslash = "/")
while (!dir.exists(file.path(root, "data_audit", "outputs")) && dirname(root) != root) root <- dirname(root)
out_dir <- file.path(root, "data_audit", "outputs", "figures_phase3_tidyplots")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
source_path <- file.path(root, "data_audit", "outputs", "figure_sources", "figure3_exercise_axis_contrasts.csv")
d <- read_csv(source_path, show_col_types = FALSE)

metric_order <- c("NAMPT_z", "inflammatory_score", "repair_score", "balance_score")
metric_labels <- c(NAMPT_z="NAMPT_z", inflammatory_score="Inflammatory", repair_score="Repair", balance_score="Balance")
contrast_order <- c("exercised_vs_rest", "active_post_vs_active_pre", "inactive_post_vs_inactive_pre", "24h_exercise_vs_control", "post_training_vs_pre_training", "MICE_active_post_vs_pre", "MICE_active_24h_vs_pre", "MICE_placebo_post_vs_pre", "MICE_placebo_24h_vs_pre", "SIE_active_post_vs_pre", "SIE_active_24h_vs_pre", "SIE_placebo_post_vs_pre", "SIE_placebo_24h_vs_pre")
contrast_labels <- c(
  exercised_vs_rest="Cycling recovery", active_post_vs_active_pre="Active + exercise",
  inactive_post_vs_inactive_pre="Inactive + exercise", `24h_exercise_vs_control`="Acute exercise, 24 h",
  post_training_vs_pre_training="Training, 6 weeks", MICE_active_post_vs_pre="MICE OLE, immediate",
  MICE_active_24h_vs_pre="MICE OLE, 24 h", MICE_placebo_post_vs_pre="MICE placebo, immediate",
  MICE_placebo_24h_vs_pre="MICE placebo, 24 h", SIE_active_post_vs_pre="SIE OLE, immediate",
  SIE_active_24h_vs_pre="SIE OLE, 24 h", SIE_placebo_post_vs_pre="SIE placebo, immediate",
  SIE_placebo_24h_vs_pre="SIE placebo, 24 h")

# Panel A: all 13 displayed contrasts, NAMPT_z only.
a <- d %>% filter(metric == "NAMPT_z") %>%
  mutate(contrast_label=factor(unname(contrast_labels[contrast]), levels=rev(unname(contrast_labels[contrast_order]))),
         paired = analysis_design != "unpaired")
stopifnot(nrow(a)==13, n_distinct(a$contrast)==13)
pa <- tidyplot(a, x=mean_delta, y=contrast_label) %>%
  add_range_errorbar() %>% add_data_points(size=2.0) %>%
  add_reference_lines(x=0, linetype="dashed", linewidth=0.3) %>%
  adjust_x_axis(title="NAMPT_z mean within-dataset change") %>%
  adjust_y_axis(title=NULL) %>% theme_tidyplot(fontsize=7.5) %>%
  adjust_title(title="Exercise-associated NAMPT induction")
pa <- pa + theme(plot.title=element_text(face="bold", size=10), axis.text.y=element_text(size=7))

# Panel B: GSE318937 balance score, immediate versus 24 h, with MICE/SIE and treatment lines.
b <- d %>% filter(dataset_id=="GSE318937_exercise_oleuropein", metric=="balance_score") %>%
  mutate(timepoint=if_else(grepl("24h", contrast),"24 h","Immediate"),
         exercise_mode=if_else(grepl("MICE", contrast),"MICE","SIE"),
         treatment=if_else(grepl("active", contrast),"OLE","Placebo"),
         trace=paste(exercise_mode,treatment,sep=" + "),
         timepoint=factor(timepoint, levels=c("Immediate","24 h")))
stopifnot(nrow(b)==8, n_distinct(b$trace)==4)
pb <- tidyplot(b, x=timepoint, y=mean_delta, group=trace, color=exercise_mode) %>%
  add_reference_lines(y=0, linetype="dashed", linewidth=0.3) %>%
  add_line(linewidth=0.55) %>% add_data_points(size=2.1) %>%
  adjust_x_axis(title=NULL) %>% adjust_y_axis(title="Balance-score delta") %>%
  theme_tidyplot(fontsize=7.5) %>% adjust_title(title="Immediate stress bias relaxes by 24 h")
pb <- pb + theme(plot.title=element_text(face="bold", size=10), legend.position="right")

# Panel C: 13 x 4 contrast-by-metric heatmap, white points indicate metric FDR < 0.10.
c <- d %>% mutate(contrast_label=factor(unname(contrast_labels[contrast]), levels=rev(unname(contrast_labels[contrast_order]))), metric_label=factor(unname(metric_labels[metric]), levels=unname(metric_labels[metric_order])), fdr=q_value_metric < 0.10)
stopifnot(nrow(c)==52, n_distinct(c$metric)==4, n_distinct(c$contrast)==13)
pc <- tidyplot(c, x=metric_label, y=contrast_label, fill=mean_delta) %>%
  add_heatmap() %>%
  add_data_points(data=filter(c,fdr), shape=21, size=1.6, white_border=TRUE) %>%
  adjust_x_axis(title=NULL, rotate_labels=35) %>% adjust_y_axis(title=NULL) %>%
  theme_tidyplot(fontsize=7.2) %>% adjust_title(title="Exercise reshapes four NAMPT-axis metrics")
pc <- pc + theme(plot.title=element_text(face="bold", size=10), legend.position="right", axis.text.y=element_text(size=6.5))

# tidyplots 0.4.0 S7 objects cannot be safely composed by patchwork in this R setup.
# Export each data-faithful panel separately at the final manuscript width instead.
# A later layout step can compose these SVGs without changing any data layers.
panel_list <- list(a=pa, b=pb, c=pc)
for (nm in names(panel_list)) {
  save_plot(panel_list[[nm]], filename=file.path(out_dir, paste0("Figure3_exercise_tidyplots_panel_", nm, ".svg")), width=183, height=72, units="mm", view_plot=FALSE)
}
base <- file.path(out_dir,"Figure3_exercise_tidyplots_panels")
writeLines(c("status=panel_exports; composite_layout_pending_due_to_tidyplots_patchwork_S7_incompatibility","panel_a_rows=13","panel_a_contrasts=13","panel_b_rows=8","panel_b_traces=4","panel_c_rows=52","panel_c_metrics=4","panel_c_contrasts=13","render_backend=tidyplots 0.4.0","width_mm=183"), paste0(base,"_qc.txt"))
message("Wrote ",base)
