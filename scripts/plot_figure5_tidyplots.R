#!/usr/bin/env Rscript
# Figure 5: obesity/weight-loss tissue and disease-background dependence.
# Cell-model contrasts are deliberately excluded from the main figure.

suppressPackageStartupMessages({library(tidyplots);library(readr);library(dplyr);library(ggplot2);library(ragg);library(svglite)})
root <- normalizePath(getwd(),winslash="/"); while(!dir.exists(file.path(root,"data_audit","outputs"))&&dirname(root)!=root) root<-dirname(root)
out<-file.path(root,"data_audit","outputs","figures_phase3_tidyplots");dir.create(out,showWarnings=FALSE,recursive=TRUE)
d<-read_csv(file.path(root,"data_audit/outputs/figure_sources/figure4_obesity_axis_contrasts.csv"),show_col_types=FALSE) %>% filter(!grepl("GSE282850",dataset_id))
metrics<-c("NAMPT_z","inflammatory_score","repair_score","balance_score"); labels<-c(NAMPT_z="NAMPT_z",inflammatory_score="Inflammatory",repair_score="Repair",balance_score="Balance")
contrasts<-c("obese_before_vs_lean","obese_after_vs_obese_before","OB_w52_vs_OB_w0","T2D_w52_vs_T2D_w0")
clab<-c(obese_before_vs_lean="Obesity vs lean monocytes",obese_after_vs_obese_before="Post-bariatric monocytes",OB_w52_vs_OB_w0="Obese muscle: week 52 vs 0",T2D_w52_vs_T2D_w0="T2D muscle: week 52 vs 0")
# Panel a: all obesity/weight-loss contrast metrics.
a<-d%>%mutate(contrast_label=factor(unname(clab[contrast]),levels=rev(unname(clab[contrasts]))),metric_label=factor(unname(labels[metric]),levels=unname(labels[metrics])))
stopifnot(nrow(a)==16,n_distinct(a$contrast)==4,n_distinct(a$metric)==4)
pa<-tidyplot(a,x=mean_delta,y=contrast_label,color=metric_label)%>%add_range_errorbar()%>%add_data_points(size=2)%>%add_reference_lines(x=0,linetype="dashed",linewidth=.3)%>%adjust_x_axis(title="Mean within-dataset change")%>%adjust_y_axis(title=NULL)%>%theme_tidyplot(fontsize=7.5)%>%adjust_title(title="Obesity and weight-loss contrasts")
# Panel b: monocyte remodeling, four metrics.
b<-d%>%filter(dataset_id=="GSE32575_monocytes_obesity_surgery",contrast=="obese_after_vs_obese_before")%>%mutate(metric_label=factor(unname(labels[metric]),levels=unname(labels[metrics])))
stopifnot(nrow(b)==4)
pb<-tidyplot(b,x=metric_label,y=mean_delta,color=metric_label)%>%add_range_errorbar()%>%add_data_points(size=2.3)%>%add_reference_lines(y=0,linetype="dashed",linewidth=.3)%>%adjust_x_axis(title=NULL,rotate_labels=25)%>%adjust_y_axis(title="Post vs pre mean delta")%>%theme_tidyplot(fontsize=8)%>%adjust_title(title="Post-bariatric monocyte remodeling")
# Panel c: skeletal muscle OB vs T2D, four metrics x two contrasts.
c<-d%>%filter(dataset_id=="GSE272133_muscle_bariatric")%>%mutate(metric_label=factor(unname(labels[metric]),levels=unname(labels[metrics])),contrast_label=factor(unname(clab[contrast]),levels=rev(unname(clab[c("OB_w52_vs_OB_w0","T2D_w52_vs_T2D_w0")]))))
stopifnot(nrow(c)==8)
pc<-tidyplot(c,x=metric_label,y=mean_delta,color=contrast_label)%>%add_range_errorbar()%>%add_data_points(size=2.1)%>%add_reference_lines(y=0,linetype="dashed",linewidth=.3)%>%adjust_x_axis(title=NULL,rotate_labels=25)%>%adjust_y_axis(title="Mean delta")%>%theme_tidyplot(fontsize=8)%>%adjust_title(title="Skeletal-muscle response by disease state")
for(nm in c("a","b","c")) save_plot(get(paste0("p",nm)),filename=file.path(out,paste0("Figure5_obesity_tidyplots_panel_",nm,".svg")),width=183,height=72,units="mm",view_plot=FALSE)
writeLines(c("status=panel_exports","main_figure_scope=obesity/weight-loss/tissue/disease only","panel_a_rows=16","panel_a_contrasts=4","panel_b_rows=4","panel_c_rows=8","cell_model_moved_to_supplement=TRUE","render_backend=tidyplots 0.4.0"),file.path(out,"Figure5_obesity_tidyplots_qc.txt"))
message("Wrote Figure 5 obesity panels to ",out)
