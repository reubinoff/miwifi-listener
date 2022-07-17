import { Component, OnInit } from '@angular/core';
import { StorageService } from '../_services/storage.service';
import { UserService } from '../_services/user.service';
import { RequestService } from '../_services/requests.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  users: string[] = [];
  selectedUser: string = '';
  errorMessage = '';
  username: string = '';
  timeSlotsList = [{ name: 15 }, { name: 30 }, { name: 45 }, { name: 60 }];
  selectedTimeSlot: number = 15;

  constructor(
    private userService: UserService,
    private storageService: StorageService,
    private requestService: RequestService,
  ) {}

  isLoggedIn = false;

  ngOnInit(): void {
    this.username = this.storageService.getUser().username;
    console.log(this.username);
    this.isLoggedIn = this.storageService.isLoggedIn();
  }

  onSubmit(): void {
    let req = new WifiRequest(
      this.username,
      Math.round(Date.now() / 1000),
      this.selectedTimeSlot
    );
    this.requestService.sendRequest(req).subscribe({
      next: data => {
        console.log(data);
      }
    });


  }
}
