import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadComponent } from './components/upload/upload.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, UploadComponent],
  template: `
    <div class="app-container">
      <header>
        <h1>🚀 ML Analytics Platform</h1>
        <p>Upload your CSV files for instant analysis</p>
      </header>
      <main>
        <app-upload></app-upload>
      </main>
    </div>
  `,
  styles: [`
    .app-container {
      min-height: 100vh;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px;
    }
    header {
      text-align: center;
      color: white;
      margin-bottom: 30px;
    }
    h1 { font-size: 2.5rem; margin-bottom: 10px; }
    p { font-size: 1.2rem; opacity: 0.9; }
  `]
})
export class AppComponent {
  title = 'ML Analytics';
}