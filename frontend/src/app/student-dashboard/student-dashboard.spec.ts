import { ComponentFixture, TestBed } from '@angular/core/testing';
import { StudentLoginComponent } from './student-login.component';

describe('StudentDashboardComponent', () => {
  let component: StudentDashboardComponent;
  let fixture: ComponentFixture<StudentDashboardComponent>;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StudentDashboardComponent], // because it is standalone
    }).compileComponents();

    fixture = TestBed.createComponent(StudentDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
