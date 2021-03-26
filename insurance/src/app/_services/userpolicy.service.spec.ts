import { TestBed } from '@angular/core/testing';

import { UserpolicyService } from './userpolicy.service';

describe('UserpolicyService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: UserpolicyService = TestBed.get(UserpolicyService);
    expect(service).toBeTruthy();
  });
});
