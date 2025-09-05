import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="upload-container">
      <div class="upload-card">
        <div class="drop-zone" [class.dragover]="isDragOver" 
             (dragover)="onDragOver($event)" 
             (dragleave)="onDragLeave($event)" 
             (drop)="onFileDropped($event)"
             (click)="fileInput.click()">
          
          <input #fileInput type="file" accept=".csv" 
                 (change)="onFileSelected($event)" hidden>
          
          <div class="upload-icon">📊</div>
          <h3>Upload CSV File</h3>
          <p>Drag & drop or click to select</p>
        </div>

        <div *ngIf="selectedFile" class="file-info">
          <h4>📁 File Selected:</h4>
          <p><strong>Name:</strong> {{selectedFile?.name}}</p>
          <p><strong>Size:</strong> {{formatFileSize(selectedFile?.size || 0)}}</p>
          
          <button class="upload-btn" (click)="uploadFile()" [disabled]="isUploading">
            <span *ngIf="!isUploading">🚀 Upload & Analyze</span>
            <span *ngIf="isUploading">⏳ Processing...</span>
          </button>
        </div>

        <div *ngIf="result" class="result-section">
          <h4>✅ Analysis Complete:</h4>
          <pre>{{formatResult(result)}}</pre>
        </div>

        <div *ngIf="error" class="error-section">
          <h4>❌ Error:</h4>
          <p>{{error}}</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .upload-container {
      display: flex;
      justify-content: center;
      padding: 20px;
    }
    .upload-card {
      background: white;
      border-radius: 15px;
      padding: 30px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.1);
      max-width: 600px;
      width: 100%;
    }
    .drop-zone {
      border: 3px dashed #ddd;
      border-radius: 10px;
      padding: 40px;
      text-align: center;
      cursor: pointer;
      transition: all 0.3s;
    }
    .drop-zone:hover, .drop-zone.dragover {
      border-color: #667eea;
      background: #f8f9ff;
    }
    .upload-icon { font-size: 3rem; margin-bottom: 15px; }
    .file-info, .result-section, .error-section {
      margin-top: 20px;
      padding: 20px;
      border-radius: 8px;
    }
    .file-info { background: #f0f8ff; }
    .result-section { background: #f0fff0; }
    .error-section { background: #fff0f0; }
    .upload-btn {
      background: #667eea;
      color: white;
      border: none;
      padding: 12px 25px;
      border-radius: 8px;
      cursor: pointer;
      font-weight: bold;
      margin-top: 15px;
    }
    .upload-btn:disabled { opacity: 0.6; }
    pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
  `]
})
export class UploadComponent {
  selectedFile: File | null = null;
  isUploading = false;
  result: any = null;
  error: string | null = null;
  isDragOver = false;

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
    this.resetResults();
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragOver = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDragOver = false;
  }

  onFileDropped(event: DragEvent) {
    event.preventDefault();
    this.isDragOver = false;
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.selectedFile = files[0];
      this.resetResults();
    }
  }

  uploadFile() {
    if (!this.selectedFile) return;

    this.isUploading = true;
    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post('http://localhost:5224/api/analyze', formData)
      .subscribe({
        next: (response) => {
          this.result = response;
          this.error = null;
          this.isUploading = false;
        },
        error: (err) => {
          this.error = 'Upload failed. Please try again.';
          this.result = null;
          this.isUploading = false;
        }
      });
  }

  formatFileSize(bytes: number): string {
    return bytes < 1024 ? bytes + ' B' : 
           bytes < 1048576 ? (bytes / 1024).toFixed(1) + ' KB' :
           (bytes / 1048576).toFixed(1) + ' MB';
  }

  formatResult(result: any): string {
    return JSON.stringify(result, null, 2);
  }

  resetResults() {
    this.result = null;
    this.error = null;
  }
}