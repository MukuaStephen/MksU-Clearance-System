import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-student-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './student-login.component.html',
  styleUrls: ['./student-login.component.css']
})
export class StudentLoginComponent {
  email: string = '';
  password: string = '';

  constructor(private router: Router) {}

  login(): void {
    if (this.email && this.password) {
      // TODO: replace with real auth service
      this.router.navigate(['/student-dashboard']);
    }
  }
}
