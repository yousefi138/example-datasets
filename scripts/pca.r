#!/usr/bin/env Rscript
#
# Simulate continuous and binary variables dataset
#
# This script reproducibly generates a dataset with continuous and binary variables
# with specifications from inst/continuous.csv and inst/binary.csv
#
args <- commandArgs(trailingOnly=TRUE)

config.name <- "local"
if (length(args) > 0)
    config.name <- args[1]

paths <- config::get(config=config.name)
print(paths)

# Set seed for reproducibility
set.seed(42)

# Number of observations
n <- 2640

# Read the continuous variables specifications
specs_continuous <- read.csv(
						file.path(paths$project,"inst/continuous.csv"), 
							stringsAsFactors = FALSE)

# Clean up special characters and trim whitespace in continuous specs
specs_continuous$variable <- trimws(specs_continuous$variable)
specs_continuous$median <- as.numeric(gsub("[^0-9.]", "", trimws(specs_continuous$median)))
specs_continuous$iqr <- trimws(specs_continuous$iqr)
specs_continuous$n_missing <- as.numeric(gsub("[^0-9]", "", trimws(specs_continuous$n_missing)))

# Generate continuous variables using Map
data_continuous <- as.data.frame(Map(function(var_name, median_val, iqr_str, n_missing) {
  # Parse IQR string to extract Q1 and Q3
  # Remove whitespace and parentheses, and convert to numeric
  iqr_clean <- gsub("[^0-9.,]", "", iqr_str)
  iqr_parts <- as.numeric(strsplit(iqr_clean, ",")[[1]])
  q1 <- iqr_parts[1]
  q3 <- iqr_parts[2]
  
  # Calculate IQR and estimate standard deviation from IQR
  # For normal distribution: IQR ≈ 1.35 * sigma
  iqr_val <- q3 - q1
  sigma <- iqr_val / 1.35
  
  # Generate normally distributed data with specified median and sigma
  values <- rnorm(n, mean = median_val, sd = sigma)
  
  # Introduce missing values
  if (n_missing > 0) {
    missing_indices <- sample(seq_len(n), size = n_missing, replace = FALSE)
    values[missing_indices] <- NA
  }
  
  values
}, specs_continuous$variable, specs_continuous$median, specs_continuous$iqr, specs_continuous$n_missing))

# Read the binary variables specifications
specs_binary <- read.csv(
						file.path(paths$project,"inst/binary.csv"), 
							stringsAsFactors = FALSE)

# Clean up special characters and trim whitespace in binary specs
specs_binary$variable <- trimws(specs_binary$variable)
specs_binary$n <- as.numeric(gsub("[^0-9]", "", trimws(specs_binary$n)))
specs_binary$n_missing <- as.numeric(gsub("[^0-9]", "", trimws(specs_binary$n_missing)))

# Generate binary variables using Map
data_binary <- as.data.frame(Map(function(var_name, n_ones, n_missing) {
  # Create vector with n_ones 1's, (n - n_ones - n_missing) 0's, and n_missing NA's
  n_zeros <- n - n_ones - n_missing
  values <- sample(c(rep(1, n_ones), rep(0, n_zeros), rep(NA, n_missing)))
  
  values
}, specs_binary$variable, specs_binary$n, specs_binary$n_missing))

# Combine continuous and binary data
data <- cbind(data_continuous, data_binary)

# Read the categorical variables specifications
specs_categorical <- read.csv(
						file.path(paths$project,"inst/categorical.csv"), 
							stringsAsFactors = FALSE)

# Clean up special characters and trim whitespace in categorical specs
specs_categorical$variable <- trimws(specs_categorical$variable)
specs_categorical$levels <- trimws(specs_categorical$levels)
specs_categorical$n <- as.numeric(gsub("[^0-9]", "", trimws(specs_categorical$n)))
specs_categorical$n_missing <- as.numeric(gsub("[^0-9]", "", trimws(specs_categorical$n_missing)))

# Get unique variable names
cat_variables <- unique(specs_categorical$variable)

# Generate categorical variables
data_categorical <- as.data.frame(Map(function(var_name) {
  # Subset specs for this variable
  var_specs <- specs_categorical[specs_categorical$variable == var_name, ]
  
  # Get unique n_missing (should be the same for all levels)
  n_missing <- var_specs$n_missing[1]
  
  # Create vector with repeated levels according to their counts
  values <- rep(var_specs$levels, times = var_specs$n)
  
  # Add missing values
  if (n_missing > 0) {
    values <- c(values, rep(NA, n_missing))
  }
  
  # Shuffle values
  values <- sample(values)
  
  values
}, cat_variables))

# Name the columns appropriately
names(data_categorical) <- cat_variables

# Combine all data (continuous, binary, and categorical)
data <- cbind(data, data_categorical)

# Display summary
cat("Generated dataset with", nrow(data), "observations and", ncol(data), "variables\n")
cat("Continuous variables:", ncol(data_continuous), "\n")
cat("Binary variables:", ncol(data_binary), "\n")
cat("Categorical variables:", ncol(data_categorical), "\n\n")
print(summary(data))

# Save the dataset
output_file <- file.path(paths$project,"data/pca.csv")
write.csv(data, file = output_file, row.names = FALSE)
cat("\nDataset saved to:", output_file, "\n")
