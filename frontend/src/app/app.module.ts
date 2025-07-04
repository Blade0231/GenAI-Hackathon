import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http'; // ✅ Only HttpClientModule here
import { LinebreaksPipe } from './pipes/linebreaks.pipe';

@NgModule({
  declarations: [
    AppComponent,LinebreaksPipe
  ],
  imports: [
    BrowserModule,
    CommonModule,
    FormsModule,
    HttpClientModule // ✅ This is enough to provide HttpClient
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }