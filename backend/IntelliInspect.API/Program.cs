var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddHttpClient();

// Add CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins("http://localhost:4200")
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("AllowFrontend");

// Fix: Call YOUR actual ML service route
app.MapPost("/api/analyze", async (IFormFile file, HttpClient httpClient) =>
{
    try
    {
        if (file == null || file.Length == 0)
        {
            return Results.BadRequest(new { error = "No file uploaded" });
        }

        using var formData = new MultipartFormDataContent();
        using var fileStream = file.OpenReadStream();
        using var streamContent = new StreamContent(fileStream);
        
        streamContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("text/csv");
        formData.Add(streamContent, "file", file.FileName);

        // Call YOUR actual route: /upload-dataset
        var response = await httpClient.PostAsync("http://localhost:8000/upload-dataset", formData);
        
        if (response.IsSuccessStatusCode)
        {
            var result = await response.Content.ReadAsStringAsync();
            return Results.Ok(System.Text.Json.JsonSerializer.Deserialize<object>(result));
        }
        else
        {
            return Results.Problem("ML service error");
        }
    }
    catch (Exception ex)
    {
        return Results.Problem(ex.Message);
    }
})
.DisableAntiforgery();

app.Run();