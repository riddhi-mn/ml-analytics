namespace IntelliInspect.API.Models
{
    public class TrainingRequest
    {
        public string TrainStart { get; set; } = string.Empty;
        public string TrainEnd { get; set; } = string.Empty;
        public string TestStart { get; set; } = string.Empty;
        public string TestEnd { get; set; } = string.Empty;
    }

    public class TrainingResponse
    {
        public double Accuracy { get; set; }
        public double Precision { get; set; }
        public double Recall { get; set; }
        public double F1Score { get; set; }
        public ConfusionMatrix ConfusionMatrix { get; set; } = new();
    }

    public class ConfusionMatrix
    {
        public int TruePositive { get; set; }
        public int TrueNegative { get; set; }
        public int FalsePositive { get; set; }
        public int FalseNegative { get; set; }
    }
}