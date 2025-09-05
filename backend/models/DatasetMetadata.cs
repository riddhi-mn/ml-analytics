namespace IntelliInspect.API.Models
{
    public class DatasetMetadata
    {
        public string Status { get; set; } = string.Empty;
        public MetadataInfo Metadata { get; set; } = new();
    }

    public class MetadataInfo
    {
        public int TotalRecords { get; set; }
        public int TotalColumns { get; set; }
        public double PassRate { get; set; }
        public string EarliestTimestamp { get; set; } = string.Empty;
        public string LatestTimestamp { get; set; } = string.Empty;
    }
}