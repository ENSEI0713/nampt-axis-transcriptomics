#!/usr/bin/env Rscript
# Figure 6 exploratory computational extension: transparent workflow + evidence gate.
# Detailed candidate/Tier tables remain supplementary.
suppressPackageStartupMessages({library(tidyplots);library(readr);library(dplyr);library(ggplot2);library(ragg);library(svglite)})
root<-normalizePath(getwd(),winslash="/"); while(!dir.exists(file.path(root,"data_audit","outputs"))&&dirname(root)!=root) root<-dirname(root)
out<-file.path(root,"data_audit","outputs","figures_phase3_tidyplots");dir.create(out,showWarnings=FALSE,recursive=TRUE)
e<-read_csv(file.path(root,"data_audit/outputs/evo2/tiers.csv"),show_col_types=FALSE)
counts<-e%>%count(tier)%>%mutate(tier=factor(tier,levels=c("A","B","C","External-only","Excluded")))
# Compact, non-causal evidence gate panel.
p<-tidyplot(counts,x=tier,y=n,fill=tier)%>%add_barstack_relative()%>%adjust_x_axis(title=NULL)%>%adjust_y_axis(title="Candidates (n)")%>%theme_tidyplot(fontsize=8)%>%adjust_title(title="Exploratory Evo2 evidence gate")
base<-file.path(out,"Figure6_evo2_exploratory_tidyplots_panel_c")
save_plot(p,filename=paste0(base,".svg"),width=183,height=72,units="mm",view_plot=FALSE)
writeLines(c("status=exploratory_supplementary_panel","rows=432","tier_A=0","tier_B=0","tier_C=97","external_only=9","excluded=326","interpretation=not validated mechanism or causal ranking","render_backend=tidyplots 0.4.0"),paste0(base,"_qc.txt"))
message("Wrote Figure 6 exploratory panel")
