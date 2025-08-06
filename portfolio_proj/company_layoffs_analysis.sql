-- Analysis

SELECT *
FROM layoffs_staging2;

SELECT MAX(total_laid_off), MAX(percentage_laid_off)
FROM layoffs_staging2;
-- Largest # laid off at a time: 12000
-- Apparently an entire company was laid off (100%)

SELECT *
FROM layoffs_staging2
WHERE percentage_laid_off = 1
ORDER BY total_laid_off DESC;
-- Companies that laid off all workers, by largest layoff amount

SELECT company, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY company
ORDER BY 2 DESC;
-- Companies with most layoffs: Amazon, Google, Meta, etc (in the 10,000s)

SELECT MIN(`date`), MAX(`date`)
FROM layoffs_staging2;
-- From 3/2020 to 3/2023

SELECT industry, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY industry
ORDER BY 2 DESC;
-- Industries that were impacted most: Consumer, Retail, Transportation, etc

SELECT country, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY country
ORDER BY 2 DESC;
-- Countries with most layoffs: US, India, Netherlands, Sweden, Brazil, etc

SELECT YEAR(`date`), SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY YEAR(`date`)
ORDER BY 1 DESC;
-- 2023 has high # of layoffs (125677)
-- 2022 had greatest # of layoffs (160322)

SELECT stage, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY stage
ORDER BY 1 DESC;
-- Higher developed companies typically have less layoffs (post IPO)

SELECT SUBSTRING(`date`, 1, 7) AS `month`, SUM(total_laid_off)
FROM layoffs_staging2
WHERE SUBSTRING(`date`, 1, 7) IS NOT NULL
GROUP BY `month`
ORDER BY 1 ASC;
-- Gives layoffs by month for each year
-- We want to do a rolling sum

WITH Rolling_Total AS 
(
SELECT SUBSTRING(`date`, 1, 7) AS `month`, SUM(total_laid_off) AS total_off
FROM layoffs_staging2
WHERE SUBSTRING(`date`, 1, 7) IS NOT NULL
GROUP BY `month`
ORDER BY 1 ASC
)
SELECT `month`, total_off, SUM(total_off) OVER(ORDER BY `month`) as rolling_total
FROM Rolling_Total;
-- Gives rolling total of layoffs

SELECT company, YEAR(`date`), SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY company, YEAR(`date`)
ORDER BY company;
-- # of Layoffs by company per year

SELECT company, YEAR(`date`), SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY company, YEAR(`date`)
ORDER BY 3 DESC;

WITH Company_Year (company, years, total_laid_off) AS
(
SELECT company, YEAR(`date`), SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY company, YEAR(`date`)
), Company_Year_Rank AS
(
SELECT *,
DENSE_RANK() OVER (PARTITION BY years ORDER BY total_laid_off DESC) AS ranking
FROM Company_Year
WHERE years IS NOT NULL
)
SELECT *
FROM Company_Year_Rank
WHERE ranking <= 10
;
-- Top 10 companies with greatest layoffs for each year
-- 2020: Uber, Booking.com, Groupon, etc
-- 2021: Bytedance, Katerra, Zillow, etc
-- 2022: Meta, Amazon, Cisco (greatest year, in 10000s)
-- 2023: Google, Microsoft, Ericsson, etc
-- Tech companies took a big hit in recent year 














