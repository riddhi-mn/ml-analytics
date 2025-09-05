namespace IntelliInspect.API.Models
{
    public class DateRangeRequest
    {
        public string TrainStart { get; set; } = string.Empty;
        public string TrainEnd { get; set; } = string.Empty;
        public string TestStart { get; set; } = string.Empty;
        public string TestEnd { get; set; } = string.Empty;
        public string SimStart { get; set; } = string.Empty;
        public string SimEnd { get; set; } = string.Empty;
    }

    public class DateRangeResponse
    {
        public string Status { get; set; } = string.Empty;
        public RangeCounts Counts { get; set; } = new();
    }

    public class RangeCounts
    {
        public int Training { get; set; }
        public int Testing { get; set; }
        public int Simulation { get; set; }
    }
}