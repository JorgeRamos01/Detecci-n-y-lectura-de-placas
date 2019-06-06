

rdat <- read.csv("results/results_evaluation_all_methods/results_plates_metrics_01.csv",
                 row.names = 1)

head(rdat)


ocr.acc <- rdat$predkenny
ocr.acc.adj <- ocr.acc
ocr.acc.adj[ocr.acc < 1e-8] <- NA
mean(ocr.acc.adj, na.rm = T)
hist(ocr.acc.adj, col = "orange")

ocr.acc.adj.qt <- quantile(ocr.acc.adj, na.rm = T)

plot(density(ocr.acc.adj, na.rm = T),
     col = "orange", lwd = 3,
     main = "Similaridad parcial",
     ylab = "Densidad",
     xlab = "Precisión del método", cex.axis = 1.5)
abline(v = median(ocr.acc.adj, na.rm = T),
       col = "red", lty = 2, lwd = 1.5)
# abline(v = ocr.acc.adj.qt[2], 
#        col = "royalblue", lty = 3,
#        lwd = 1.3)
# abline(v = ocr.acc.adj.qt[4], 
#        col = "royalblue", lty = 3,
#        lwd = 1.3)
legend("topleft", legend = c("Densidad", "Mediana"),
       col = c("orange", "red"),
       lwd = c(3, 2),
       lty = c(1, 2))
grid(col = "gray")

