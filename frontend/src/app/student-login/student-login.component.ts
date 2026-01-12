import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-student-login',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './student-login.component.html',
  styleUrls: ['./student-login.component.css']
})
export class StudentLoginComponent {

  constructor(private router: Router) {}

  login() {
    this.router.navigate(['/dashboard']);
  }
}
