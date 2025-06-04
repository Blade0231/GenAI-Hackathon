import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { LinebreaksPipe } from './pipes/linebreaks.pipe';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule, LinebreaksPipe],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements AfterViewInit {
  videoPath = 'assets/neuralnet.mp4';
  showPrompt = false;
  userPrompt = '';
  chatMessages: string[] = [];
  isProcessing = false;
  fileAttachment: File | null = null;

  @ViewChild('inputField') inputField!: ElementRef;
  @ViewChild('bgVideo') bgVideo!: ElementRef<HTMLVideoElement>;
  @ViewChild('inputArea') inputArea!: ElementRef<HTMLTextAreaElement>;

  sections = [
    {
      title: 'Multi-Agent AI System for Smart Incident Recovery',
      points: [],
      image: 'assets/brain.png'
    },
    {
      title: 'Problem Statement',
      points: [
        'Empowering IT support with Gen AI based Multi-Agent Bot for faster issue resolution and Smart Task Automation',
        'Barclays manages over 3500 service offerings, each essential to daily customer and client operations.',
        'In 2025, on an avg 11,000/week Standard incidents are generated as of today, which includes System as well as User generated Incidents causing service discruption leading to customer impact.'
      ],
      image: 'assets/brain.png'
    },
    {
      title: 'Solution & Tech Stack',
      points: [
        'AI assistant automates event detection, knowledge lookup, and resolution steps.',
        'Built with GPT-4o and LangGraph for intelligent orchestration.',
        'Powered by FastAPI backend, Angular frontend, and Azure Cloud deployment.'
      ],
      image: 'assets/brain.png'
    },
    {
      title: 'Architecture',
      points: [],
      image: 'assets/WatchTower.drawio.png'
    }
  ];



  constructor(private http: HttpClient) { }

  ngAfterViewInit() {
    const videoEl = this.bgVideo?.nativeElement;
    if (videoEl) {
      videoEl.muted = true;
      //videoEl.play().catch(() => {});
    }
  }

  togglePrompt() {
    this.showPrompt = !this.showPrompt;
    setTimeout(() => this.scrollToBottom(), 0);
  }

  closePrompt() {
    this.showPrompt = false;
  }

  scrollToBottom() {
    const container = document.querySelector('.chat-messages');
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }

  handleFileInput(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.fileAttachment = input.files[0];
      input.value = ''; // allows reuploading same file again
    }
  }

  async onPromptSubmit(promptValue: string) {
    const textarea = this.inputArea?.nativeElement;
    if (textarea) {
      textarea.style.height = 'auto';
    }

    if ((!promptValue.trim() && !this.fileAttachment) || this.isProcessing) return;

    if (promptValue.trim()) {
      this.chatMessages.push(`🧑 You: ${promptValue}`);
    }

    if (this.fileAttachment) {
      this.chatMessages.push(`🧑 You uploaded: ${this.fileAttachment.name}`);
      console.log(this.chatMessages)
    }

    this.userPrompt = '';
    this.fileAttachment = null;
    this.isProcessing = true;

    const initial_state = { incident_raw_text: promptValue };

    try {
      this.chatMessages.push(`🤖 AI: Processing...`);
      const response = await this.http.post<any>('http://74.224.102.204:5000/execute',initial_state).toPromise();

      console.log(response);
      // let msg = response.final_response;

      this.chatMessages.pop();
      this.chatMessages.push('🤖 AI: ' + response || 'No response received');
    } catch (error) {
      this.chatMessages.pop();
      this.chatMessages.push('Something went wrong. Please try again.');
      console.error(error);
    }

    this.isProcessing = false;
    this.scrollToBottom();

  }

  handleKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); // Prevent newline
      this.onPromptSubmit(this.userPrompt);
    }
  }

  autoGrow(textarea: HTMLTextAreaElement): void {
    textarea.style.height = 'auto'; // Reset height
    textarea.style.height = textarea.scrollHeight + 'px'; // Set to content height
  }
}