import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
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
      title: 'Intro to Neural Networks',
      points: [
        'Inspired by the human brain.',
        'Built with layers of artificial neurons.',
        'Each neuron receives input, processes it, and passes it on.'
      ],
      image: 'assets/brain.png'
    },
    {
      title: 'Training Process',
      points: [
        'Requires large amounts of data.',
        'Backpropagation used to update weights.',
        'Loss functions measure prediction error.'
      ],
      image: 'assets/brain.png'
    },
    {
      title: 'Applications of Neural Networks',
      points: [
        'Used in image and speech recognition.',
        'Supports language translation and chatbots.',
        'Enables self-driving cars and smart assistants.'
      ],
      image: 'assets/brain.png'
    },
    {
      title: 'Challenges',
      points: [
        'Needs powerful GPUs or TPUs.',
        'Can overfit small datasets.',
        'Hard to interpret complex models.'
      ],
      image: 'assets/brain.png'
    },
    {
      title: 'Future Potential',
      points: [
        'Combining with symbolic AI for better reasoning.',
        'Deploying models on edge devices.',
        'Evolving into more autonomous systems.'
      ],
      image: 'assets/brain.png'
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
      const response = await this.http.post<any>('http://127.0.0.1:8000/execute', initial_state).toPromise();

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