#!/usr/bin/env Rscript
# Tidyplots prototype: exercise NAMPT_z contrast-level forest plot.
# This is a data-faithful prototype, not yet the final Figure 3 redesign.

suppressPackageStartupMessages({
  library(tidyplots)
  library(readr)
  library(dplyr)
  library(ggplot2)
  library(ragg)
  library(svglite)
})

root <- normalizePath(file.path(dirname(commandArgs(trailingOnly = FALSE)[grepl("^--file=", commandArgs(trailingOnly = FALSE))][1]), ".."), winslash = "/")
if (is.na(root) || !dir.exists(file.path(root, "data_audit", "outputs"))) root <- normalizePath(getwd(), winslash = "/")
source_path <- file.path(root, "data_audit", "outputs", "figure_sources", "figure3_exercise_axis_contrasts.csv")
out_dir <- file.path(root, "data_audit", "outputs", "figures_phase3_tidyplots")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

d <- readr::read_csv(source_path, show_col_types = FALSE) %>%
  filter(metric == "NAMPT_z") %>%
  mutate(
    contrast_label = gsub("_", " ", contrast),
    contrast_label = factor(contrast_label, levels = rev(unique(contrast_label))),
    evidence = case_when(
      q_value_metric < 0.10 ~ "FDR < 0.10",
      ci95_low * ci95_high > 0 ~ "CI excludes 0",
      TRUE ~ "Directional"
    )
  )

# Use tidyplots for the plot object and layer construction.
p <- tidyplot(d, x = mean_delta, y = contrast_label) %>%
  add_range_errorbar() %>%
  add_data_points(size = 2.2) %>%
  add_reference_lines(x = 0, linetype = "dashed", linewidth = 0.3) %>%
  adjust_x_axis(title = "NAMPT_z mean within-dataset change") %>%
  adjust_y_axis(title = NULL) %>%
  adjust_size(width = 183, height = 118, unit = "mm") %>%
  theme_tidyplot(fontsize = 8) %>%
  adjust_title(title = "Exercise-associated NAMPT induction")

# Save a reproducible vector and raster output.
svglite::svglite(file.path(out_dir, "exercise_NAMPT_z_tidyplots.svg"), width = 183 / 25.4, height = 118 / 25.4)
print(p)
dev.off()
ragg::agg_tiff(file.path(out_dir, "exercise_NAMPT_z_tidyplots.tiff"), width = 183, height = 118, units = "mm", res = 600, compression = "lzw")
print(p)
dev.off()
writeLines(c(
  paste0("source_rows=", nrow(d)),
  paste0("source_contrasts=", length(unique(d$contrast))),
  "metric=NAMPT_z",
  "render_backend=tidyplots 0.4.0",
  "status=prototype; not final Figure 3"
), file.path(out_dir, "exercise_NAMPT_z_tidyplots_qc.txt"))
message("Wrote tidyplots prototype to ", out_dir)
