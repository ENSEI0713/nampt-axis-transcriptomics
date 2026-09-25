#!/usr/bin/env Rscript
# Figure 4: cross-dataset validation of the NAMPT axis.
# Panels: contrast-level meta, dataset-level cluster-aware sensitivity, LODO.

suppressPackageStartupMessages({
  library(tidyplots); library(readr); library(dplyr); library(tidyr)
  library(ggplot2); library(ragg); library(svglite)
})
root <- normalizePath(getwd(), winslash="/")
while (!dir.exists(file.path(root,"data_audit","outputs")) && dirname(root)!=root) root <- dirname(root)
out <- file.path(root,"data_audit","outputs","figures_phase3_tidyplots"); dir.create(out,showWarnings=FALSE,recursive=TRUE)
meta <- read_csv(file.path(root,"data_audit/outputs/meta/meta_results.csv"),show_col_types=FALSE)
dset <- read_csv(file.path(root,"data_audit/outputs/meta/meta_sensitivity_dataset_level.csv"),show_col_types=FALSE)
lodo <- read_csv(file.path(root,"data_audit/outputs/meta/meta_sensitivity_lodo.csv"),show_col_types=FALSE)
metric_order <- c("NAMPT_z","inflammatory_score","repair_score","balance_score")
metric_labels <- c(NAMPT_z="NAMPT_z", inflammatory_score="Inflammatory", repair_score="Repair", balance_score="Balance")

# Panel A: primary contrast-level pooled effects. Cell model is retained but visually flagged in data.
a <- meta %>% mutate(metric_label=factor(unname(metric_labels[metric]),levels=unname(metric_labels[metric_order])), domain=factor(domain,levels=c("exercise","obesity","obesity_cell_model")), evidence=if_else(ci95_low*ci95_high>0,"CI excludes 0","Directional"), label=paste0("k=",k,"; I²=",round(I2_pct),"%"))
stopifnot(nrow(a)==12)
pa <- tidyplot(a,x=pooled_effect,y=metric_label,color=domain) %>% add_range_errorbar() %>% add_data_points(size=2.2) %>% add_reference_lines(x=0,linetype="dashed",linewidth=.3) %>% adjust_x_axis(title="Contrast-level random-effects estimate") %>% adjust_y_axis(title=NULL) %>% theme_tidyplot(fontsize=8) %>% adjust_title(title="Primary contrast-level meta-analysis")

# Panel B: dataset-level sensitivity (exercise + obesity; cell model deliberately absent).
b <- dset %>% filter(domain %in% c("exercise","obesity")) %>% mutate(metric_label=factor(unname(metric_labels[metric]),levels=unname(metric_labels[metric_order])),domain=factor(domain,levels=c("exercise","obesity")))
stopifnot(nrow(b)==8)
pb <- tidyplot(b,x=pooled,y=metric_label,color=domain) %>% add_range_errorbar() %>% add_data_points(size=2.2) %>% add_reference_lines(x=0,linetype="dashed",linewidth=.3) %>% adjust_x_axis(title="Dataset-level estimate") %>% adjust_y_axis(title=NULL) %>% theme_tidyplot(fontsize=8) %>% adjust_title(title="Cluster-aware dataset-level sensitivity")

# Panel C: LODO robustness.
c <- lodo %>% mutate(metric_label=factor(unname(metric_labels[metric]),levels=unname(metric_labels[metric_order])),dropped=factor(dropped),ci_cross=lo*hi<=0)
stopifnot(nrow(c)==16)
pc <- tidyplot(c,x=pooled,y=dropped,color=metric_label) %>% add_range_errorbar() %>% add_data_points(size=1.9) %>% add_reference_lines(x=0,linetype="dashed",linewidth=.3) %>% adjust_x_axis(title="LODO pooled estimate") %>% adjust_y_axis(title=NULL) %>% theme_tidyplot(fontsize=7.5) %>% adjust_title(title="Leave-one-dataset-out robustness")

# Export panels separately; S7 + patchwork composite is handled by SVG composition script.
for (nm in c("a","b","c")) save_plot(get(paste0("p",nm)),filename=file.path(out,paste0("Figure4_meta_tidyplots_panel_",nm,".svg")),width=183,height=72,units="mm",view_plot=FALSE)
writeLines(c("status=panel_exports","panel_a_rows=12","panel_b_rows=8","panel_c_rows=16","render_backend=tidyplots 0.4.0","panel_a_scope=contrast-level meta; cell-model retained as one dataset directional evidence","panel_b_scope=exercise and obesity dataset-level sensitivity","panel_c_scope=exercise LODO"),file.path(out,"Figure4_meta_tidyplots_qc.txt"))
message("Wrote Figure 4 tidyplots panels to ",out)
