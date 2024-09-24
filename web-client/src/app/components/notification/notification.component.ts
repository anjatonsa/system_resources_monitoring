import { Component } from '@angular/core';
import { SocketService } from '../../services/socket/socket.service';
import { CommonModule } from '@angular/common'; 

interface Notification {
  timeReceived: Date;
  messages: string[];
}

@Component({
  selector: 'app-notification',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './notification.component.html',
  styleUrl: './notification.component.css'
})
export class NotificationComponent {
  
  notifications: Notification[] = [];

  constructor(private socketService: SocketService) {}

  ngOnInit(): void {
    this.socketService.getMessages().subscribe((data: any) => {
      console.log(data)
      const newNotification: Notification = {
        timeReceived: data.time,
        messages: []
      };

      if (data.cpu_load) {
        newNotification.messages.push(data.cpu_load_message +" " + data.cpu_load);
      }
      if (data.power) {
        newNotification.messages.push(data.power_message + " " + data.power);
      }
      console.log("new notf", newNotification)
      this.notifications.unshift(newNotification);
      if (this.notifications.length > 5) {
        this.notifications.pop();
      }
    });
  }


}
