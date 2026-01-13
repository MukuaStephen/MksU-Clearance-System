import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClearanceOffice, ClearanceOfficeListComponent } from './clearance-office-list.component';

describe('ClearanceOfficeList', () => {
  let component: ClearanceOfficeListComponent;
  let fixture: ComponentFixture<ClearanceOfficeListComponent>;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClearanceOfficeListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ClearanceOfficeListComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
