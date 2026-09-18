#!/usr/bin/env Rscript
# Publication-oriented R figures for the NAMPT-axis public-data analysis.

required_packages <- c(
  "ggplot2", "patchwork", "dplyr", "tidyr", "readr",
  "scales", "svglite", "ragg"
)
missing_packages <- required_packages[
  !vapply(required_packages, requireNamespace, logical(1), quietly = TRUE)
]
if (length(missing_packages) > 0) {
  stop(
    "Missing required R packages: ", paste(missing_packages, collapse = ", "),
    ". Install them before rendering manuscript figures.",
    call. = FALSE
  )
}

suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(dplyr)
  library(tidyr)
  library(readr)
  library(scales)
})

if (requireNamespace("tidyplots", quietly = TRUE)) {
  message("tidyplots detected; using ggplot2/patchwork for controlled manuscript export.")
}

script_args <- commandArgs(trailingOnly = FALSE)
script_file <- sub("^--file=", "", script_args[grepl("^--file=", script_args)])

find_project_root <- function(start_dir) {
  current <- normalizePath(start_dir, winslash = "/", mustWork = TRUE)
  repeat {
    if (dir.exists(file.path(current, "data_audit", "outputs"))) {
      return(current)
    }
    parent <- dirname(current)
    if (identical(parent, current)) {
      stop(
        "Could not locate project root containing data_audit/outputs. ",
        "Run this script from the evo2-40b workspace root or scripts directory.",
        call. = FALSE
      )
    }
    current <- parent
  }
}

root_dir <- if (length(script_file) > 0) {
  normalizePath(file.path(dirname(script_file[1]), ".."), winslash = "/", mustWork = TRUE)
} else {
  find_project_root(getwd())
}

output_dir <- file.path(root_dir, "data_audit", "outputs")
figure_source_dir <- file.path(output_dir, "figure_sources")
figure_out_dir <- file.path(output_dir, "figures_phase2")
dir.create(figure_out_dir, showWarnings = FALSE, recursive = TRUE)

figure2_path <- file.path(figure_source_dir, "figure2_dataset_coverage.csv")
figure3_path <- file.path(figure_source_dir, "figure3_exercise_axis_contrasts.csv")
figure4_path <- file.path(figure_source_dir, "figure4_obesity_axis_contrasts.csv")
formal_stats_path <- file.path(output_dir, "nampt_axis_formal_contrast_stats.csv")

coverage <- readr::read_csv(figure2_path, show_col_types = FALSE)
exercise <- readr::read_csv(figure3_path, show_col_types = FALSE)
obesity <- readr::read_csv(figure4_path, show_col_types = FALSE)
stats_all <- readr::read_csv(formal_stats_path, show_col_types = FALSE)

num_cols <- c(
  "samples", "axis_genes_detected", "axis_gene_total", "axis_gene_coverage_pct",
  "analysis_n", "paired_n", "analysis_n_control", "analysis_n_case",
  "control_n_raw", "case_n_raw", "mean_delta", "ci95_low", "ci95_high",
  "p_value", "q_value_metric", "effect_size"
)

as_numeric_cols <- function(data) {
  data %>% mutate(across(any_of(num_cols), as.numeric))
}

coverage <- as_numeric_cols(coverage)
exercise <- as_numeric_cols(exercise)
obesity <- as_numeric_cols(obesity)
stats_all <- as_numeric_cols(stats_all)

metric_order <- c("NAMPT_z", "inflammatory_score", "repair_score", "balance_score")
metric_label_map <- c(
  NAMPT_z = "NAMPT mRNA\n(z)",
  inflammatory_score = "Inflammatory\nscore",
  repair_score = "Repair / metabolic\nscore",
  balance_score = "Balance\n(repair - inflammatory)"
)

dataset_label_map <- c(
  GSE312393_24h_exercise = "GSE312393\nacute exercise",
  GSE312393_6weeks_training = "GSE312393\n6-week training",
  GSE305038_activity_inactivity_exercise = "GSE305038\nactivity state",
  GSE292369_exercise_ketone_recovery = "GSE292369\nketone recovery",
  GSE318937_exercise_oleuropein = "GSE318937\nexercise + OLE",
  GSE32575_monocytes_obesity_surgery = "GSE32575\nmonocytes",
  GSE272133_muscle_bariatric = "GSE272133\nmuscle bariatric",
  GSE282850_muscle_cell_aicar_palmitate = "GSE282850\nmyotube stress",
  GSE294150_visceral_adipose = "GSE294150\nvisceral adipose"
)

contrast_label_map <- c(
  `24h_exercise_vs_control` = "Eccentric exercise, 24 h",
  post_training_vs_pre_training = "Resistance training, 6 weeks",
  active_post_vs_active_pre = "Normal activity + exercise",
  inactive_post_vs_inactive_pre = "Reduced activity + exercise",
  exercised_vs_rest = "Cycling recovery",
  MICE_placebo_post_vs_pre = "MICE placebo, immediate",
  MICE_placebo_24h_vs_pre = "MICE placebo, 24 h",
  MICE_active_post_vs_pre = "MICE OLE, immediate",
  MICE_active_24h_vs_pre = "MICE OLE, 24 h",
  SIE_placebo_post_vs_pre = "SIE placebo, immediate",
  SIE_placebo_24h_vs_pre = "SIE placebo, 24 h",
  SIE_active_post_vs_pre = "SIE OLE, immediate",
  SIE_active_24h_vs_pre = "SIE OLE, 24 h",
  obese_before_vs_lean = "Obesity vs lean monocytes",
  obese_after_vs_obese_before = "Post-bariatric vs pre monocytes",
  OB_w52_vs_OB_w0 = "Obesity muscle, week 52 vs 0",
  T2D_w52_vs_T2D_w0 = "T2D muscle, week 52 vs 0",
  aicar_vs_differentiated = "AICAR vs differentiated myotubes",
  palmitate_vs_differentiated = "Palmitate vs differentiated myotubes"
)

label_from_map <- function(x, mapping) {
  y <- unname(mapping[x])
  ifelse(is.na(y), gsub("_", " ", x), y)
}

theme_nature_contract <- function(base_size = 6.4, base_family = "Arial") {
  theme_classic(base_size = base_size, base_family = base_family) +
    theme(
      axis.line = element_line(linewidth = 0.32, colour = "#272727"),
      axis.ticks = element_line(linewidth = 0.32, colour = "#272727"),
      axis.title = element_text(size = base_size, colour = "#272727"),
      axis.text = element_text(size = base_size - 0.4, colour = "#272727"),
      legend.title = element_text(size = base_size - 0.2),
      legend.text = element_text(size = base_size - 0.5),
      legend.key.height = grid::unit(3.2, "mm"),
      legend.key.width = grid::unit(4.8, "mm"),
      strip.background = element_blank(),
      strip.text = element_text(size = base_size - 0.1, face = "bold"),
      plot.title = element_text(size = base_size + 0.7, face = "bold", hjust = 0),
      plot.subtitle = element_text(size = base_size - 0.1, colour = "#4D4D4D", hjust = 0),
      plot.tag = element_text(size = base_size + 1.3, face = "bold"),
      panel.grid = element_blank()
    )
}

theme_set(theme_nature_contract())

palette_contract <- c(
  neutral_dark = "#272727",
  neutral_mid = "#767676",
  neutral_light = "#D8D8D8",
  blue = "#0F4D92",
  teal = "#33B5A5",
  red = "#B64342",
  orange = "#E28E2C",
  violet = "#6A51A3"
)

metric_palette <- c(
  NAMPT_z = palette_contract[["blue"]],
  inflammatory_score = palette_contract[["red"]],
  repair_score = palette_contract[["teal"]],
  balance_score = palette_contract[["violet"]]
)

status_palette <- c(
  "FDR < 0.10" = palette_contract[["blue"]],
  "CI excludes 0" = palette_contract[["orange"]],
  "Directional" = palette_contract[["neutral_mid"]]
)

prepare_stats <- function(data) {
  data %>%
    mutate(
      dataset_label = factor(label_from_map(dataset_id, dataset_label_map)),
      contrast_label = label_from_map(contrast, contrast_label_map),
      metric_label = factor(
        unname(metric_label_map[metric]),
        levels = unname(metric_label_map[metric_order])
      ),
      evidence_status = case_when(
        q_value_metric < 0.10 ~ "FDR < 0.10",
        ci95_low * ci95_high > 0 ~ "CI excludes 0",
        TRUE ~ "Directional"
      ),
      evidence_status = factor(evidence_status, levels = names(status_palette)),
      direction_class = case_when(
        mean_delta > 0 ~ "positive",
        mean_delta < 0 ~ "negative",
        TRUE ~ "zero"
      )
    )
}

exercise <- prepare_stats(exercise)
obesity <- prepare_stats(obesity)
stats_all <- prepare_stats(stats_all)

save_pub_r <- function(plot, filename, width_mm = 183, height_mm = 120, dpi = 600) {
  w <- width_mm / 25.4
  h <- height_mm / 25.4
  base <- file.path(figure_out_dir, filename)

  svglite::svglite(paste0(base, ".svg"), width = w, height = h)
  print(plot)
  dev.off()

  grDevices::cairo_pdf(paste0(base, ".pdf"), width = w, height = h, family = "Arial")
  print(plot)
  dev.off()

  ragg::agg_tiff(paste0(base, ".tiff"), width = w, height = h, units = "in", res = dpi)
  print(plot)
  dev.off()

  ragg::agg_png(paste0(base, ".png"), width = w, height = h, units = "in", res = 300)
  print(plot)
  dev.off()
}

forest_plot <- function(data, metric_id, title, subtitle = NULL) {
  plot_data <- data %>%
    filter(metric == metric_id) %>%
    arrange(mean_delta) %>%
    mutate(contrast_label = factor(contrast_label, levels = unique(contrast_label)))

  ggplot(plot_data, aes(y = contrast_label, x = mean_delta)) +
    geom_vline(xintercept = 0, linewidth = 0.35, linetype = "dashed", colour = "#9A9A9A") +
    geom_segment(
      aes(x = ci95_low, xend = ci95_high, yend = contrast_label, colour = evidence_status),
      linewidth = 0.62, lineend = "round"
    ) +
    geom_point(aes(fill = evidence_status, size = analysis_n), shape = 21, colour = "white", stroke = 0.25) +
    scale_colour_manual(values = status_palette, drop = FALSE) +
    scale_fill_manual(values = status_palette, drop = FALSE) +
    scale_size_continuous(range = c(1.8, 4.2), breaks = c(4, 10, 16, 24), name = "Analysis n") +
    labs(x = "Mean within-dataset change", y = NULL, title = title, subtitle = subtitle, colour = NULL, fill = NULL) +
    theme(legend.position = "right")
}

heatmap_plot <- function(data, title) {
  plot_data <- data %>%
    mutate(
      contrast_label = factor(contrast_label, levels = rev(unique(contrast_label))),
      metric_label = factor(metric_label, levels = unname(metric_label_map[metric_order]))
    )

  ggplot(plot_data, aes(x = metric_label, y = contrast_label, fill = mean_delta)) +
    geom_tile(colour = "white", linewidth = 0.32) +
    geom_point(
      data = plot_data %>% filter(q_value_metric < 0.10),
      aes(x = metric_label, y = contrast_label),
      shape = 21, size = 1.55, stroke = 0.28, colour = "#272727", fill = "white"
    ) +
    scale_fill_gradient2(
      low = "#3B6EA8", mid = "white", high = "#B64342",
      midpoint = 0, name = "Mean\ndelta"
    ) +
    labs(x = NULL, y = NULL, title = title, subtitle = "White dots indicate metric-level FDR < 0.10") +
    theme(
      axis.text.x = element_text(angle = 35, hjust = 1, vjust = 1),
      legend.position = "right"
    )
}

# Figure 2: data and analysis framework -----------------------------------
coverage_plot_data <- coverage %>%
  mutate(
    dataset_label = factor(label_from_map(dataset_id, dataset_label_map)),
    module_group = case_when(
      grepl("exercise", module, ignore.case = TRUE) ~ "Exercise",
      grepl("obesity|weight", module, ignore.case = TRUE) ~ "Obesity / weight loss",
      grepl("cell", module, ignore.case = TRUE) ~ "Cell model",
      TRUE ~ "Other"
    ),
    module_group = factor(module_group, levels = c("Exercise", "Obesity / weight loss", "Cell model", "Other"))
  ) %>%
  arrange(module_group, desc(axis_gene_coverage_pct), dataset_id) %>%
  mutate(dataset_label = factor(dataset_label, levels = rev(unique(dataset_label))))

design_summary <- stats_all %>%
  distinct(dataset_id, contrast, analysis_design, analysis_n, paired_n, control_n_raw, case_n_raw) %>%
  mutate(
    design_group = case_when(
      startsWith(analysis_design, "paired") ~ "Paired/intersection",
      startsWith(analysis_design, "unpaired") ~ "Unpaired",
      TRUE ~ "Other"
    ),
    design_group = factor(design_group, levels = c("Paired/intersection", "Unpaired", "Other"))
  )

evidence_counts <- stats_all %>%
  mutate(ci_supported = ci95_low * ci95_high > 0, fdr_supported = q_value_metric < 0.10) %>%
  group_by(metric, metric_label) %>%
  summarise(
    `CI excludes 0` = sum(ci_supported, na.rm = TRUE),
    `FDR < 0.10` = sum(fdr_supported, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  pivot_longer(c(`CI excludes 0`, `FDR < 0.10`), names_to = "support_type", values_to = "n_contrasts") %>%
  mutate(
    support_type = factor(support_type, levels = c("CI excludes 0", "FDR < 0.10")),
    metric_label = factor(metric_label, levels = unname(metric_label_map[metric_order]))
  )

p2a <- ggplot(coverage_plot_data, aes(y = dataset_label, x = axis_gene_coverage_pct)) +
  geom_segment(aes(x = 0, xend = axis_gene_coverage_pct, yend = dataset_label), colour = "#D8D8D8", linewidth = 0.45) +
  geom_point(aes(size = samples, fill = module_group), shape = 21, colour = "white", stroke = 0.25) +
  scale_fill_manual(values = c("#0F4D92", "#B64342", "#33B5A5", "#767676"), drop = FALSE) +
  scale_size_continuous(range = c(2.2, 6.2), name = "Samples") +
  scale_x_continuous(limits = c(0, 105), breaks = c(0, 50, 100), labels = function(x) paste0(x, "%")) +
  labs(x = "NAMPT-axis gene coverage", y = NULL, title = "Public transcriptomic evidence base", fill = NULL) +
  theme(legend.position = "right")

p2b <- design_summary %>%
  count(design_group, name = "n_contrasts") %>%
  ggplot(aes(x = design_group, y = n_contrasts, fill = design_group)) +
  geom_col(width = 0.58, colour = "white", linewidth = 0.25) +
  geom_text(aes(label = n_contrasts), vjust = -0.45, size = 2.1, family = "Arial") +
  scale_fill_manual(values = c("#0F4D92", "#767676", "#D8D8D8"), guide = "none") +
  scale_y_continuous(expand = expansion(mult = c(0, 0.16)), breaks = pretty_breaks(n = 4)) +
  labs(x = NULL, y = "Contrasts", title = "Analysis design") +
  theme(axis.text.x = element_text(angle = 20, hjust = 1))

p2c <- ggplot(evidence_counts, aes(x = metric_label, y = n_contrasts, fill = support_type)) +
  geom_col(position = position_dodge(width = 0.62), width = 0.54, colour = "white", linewidth = 0.25) +
  scale_fill_manual(values = c("CI excludes 0" = "#E28E2C", "FDR < 0.10" = "#0F4D92")) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.12)), breaks = pretty_breaks(n = 4)) +
  labs(x = NULL, y = "Contrasts", title = "Evidence density by axis metric", fill = NULL) +
  theme(axis.text.x = element_text(angle = 25, hjust = 1), legend.position = "top")

fig2 <- (p2a | (p2b / p2c)) +
  plot_layout(widths = c(1.45, 1), guides = "collect") +
  plot_annotation(tag_levels = "a") &
  theme(legend.position = "right")

save_pub_r(fig2, "figure2_public_data_framework", width_mm = 183, height_mm = 118)

# Figure 3: exercise response ------------------------------------------------
exercise_order <- c(
  "Eccentric exercise, 24 h",
  "Resistance training, 6 weeks",
  "Normal activity + exercise",
  "Reduced activity + exercise",
  "Cycling recovery",
  "MICE placebo, immediate",
  "MICE placebo, 24 h",
  "MICE OLE, immediate",
  "MICE OLE, 24 h",
  "SIE placebo, immediate",
  "SIE placebo, 24 h",
  "SIE OLE, immediate",
  "SIE OLE, 24 h"
)
exercise <- exercise %>% mutate(contrast_label = factor(contrast_label, levels = exercise_order))

p3a <- forest_plot(
  exercise,
  metric_id = "NAMPT_z",
  title = "Exercise-associated NAMPT induction",
  subtitle = "Permutation tests with bootstrap 95% confidence intervals"
)

p3b <- heatmap_plot(exercise, title = "Exercise reshapes inflammatory and repair programs")

time_balance <- exercise %>%
  filter(dataset_id == "GSE318937_exercise_oleuropein", metric == "balance_score") %>%
  mutate(
    timepoint = ifelse(grepl("24h", contrast), "24 h", "Immediate"),
    timepoint = factor(timepoint, levels = c("Immediate", "24 h")),
    exercise_mode = ifelse(grepl("MICE", contrast), "MICE", "SIE"),
    treatment = ifelse(grepl("active", contrast), "OLE", "Placebo"),
    trace = interaction(exercise_mode, treatment, sep = " + ")
  )

p3c <- ggplot(time_balance, aes(x = timepoint, y = mean_delta, group = trace, colour = exercise_mode, linetype = treatment)) +
  geom_hline(yintercept = 0, linewidth = 0.35, linetype = "dashed", colour = "#9A9A9A") +
  geom_line(linewidth = 0.55, alpha = 0.85) +
  geom_segment(aes(y = ci95_low, yend = ci95_high, xend = timepoint), linewidth = 0.45, alpha = 0.8) +
  geom_point(aes(fill = evidence_status), shape = 21, size = 2.4, colour = "white", stroke = 0.25) +
  scale_colour_manual(values = c(MICE = "#0F4D92", SIE = "#B64342")) +
  scale_fill_manual(values = status_palette, drop = FALSE) +
  labs(
    x = NULL, y = "Balance-score delta",
    title = "Immediate stress bias relaxes by 24 h",
    colour = "Exercise", linetype = "Supplement", fill = NULL
  ) +
  theme(legend.position = "right")

fig3 <- (p3a | p3c) / p3b +
  plot_layout(heights = c(1, 1.18), guides = "collect") +
  plot_annotation(tag_levels = "a") &
  theme(legend.position = "right")

save_pub_r(fig3, "figure3_exercise_nampt_axis", width_mm = 183, height_mm = 152)

# Figure 4: obesity, weight loss, and metabolic stress ----------------------
obesity_order <- c(
  "Obesity vs lean monocytes",
  "Post-bariatric vs pre monocytes",
  "Obesity muscle, week 52 vs 0",
  "T2D muscle, week 52 vs 0",
  "AICAR vs differentiated myotubes",
  "Palmitate vs differentiated myotubes"
)
obesity <- obesity %>% mutate(contrast_label = factor(contrast_label, levels = obesity_order))

p4a <- forest_plot(
  obesity,
  metric_id = "NAMPT_z",
  title = "Obesity and metabolic stress alter NAMPT expression",
  subtitle = "Lean controls were collapsed to independent participant means where duplicated"
)

p4b <- heatmap_plot(obesity, title = "Obesity-linked states show heterogeneous axis remodeling")

monocyte_remodel <- obesity %>%
  filter(dataset_id == "GSE32575_monocytes_obesity_surgery", contrast == "obese_after_vs_obese_before") %>%
  mutate(metric_label = factor(metric_label, levels = unname(metric_label_map[metric_order])))

p4c <- ggplot(monocyte_remodel, aes(x = metric_label, y = mean_delta, colour = evidence_status, fill = metric)) +
  geom_hline(yintercept = 0, linewidth = 0.35, linetype = "dashed", colour = "#9A9A9A") +
  geom_segment(aes(y = ci95_low, yend = ci95_high, xend = metric_label), linewidth = 0.62, lineend = "round") +
  geom_point(shape = 21, size = 3.0, colour = "white", stroke = 0.25) +
  scale_colour_manual(values = status_palette, drop = FALSE) +
  scale_fill_manual(values = metric_palette, guide = "none") +
  labs(
    x = NULL, y = "Post vs pre mean delta",
    title = "Post-bariatric monocyte remodeling",
    colour = NULL
  ) +
  theme(axis.text.x = element_text(angle = 25, hjust = 1), legend.position = "right")

fig4 <- (p4a | p4c) / p4b +
  plot_layout(heights = c(1, 1.12), guides = "collect") +
  plot_annotation(tag_levels = "a") &
  theme(legend.position = "right")

save_pub_r(fig4, "figure4_obesity_nampt_axis", width_mm = 183, height_mm = 144)

message("Finished exporting Phase 2 figures to: ", figure_out_dir)
