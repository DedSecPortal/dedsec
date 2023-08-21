import wx
import socket
import requests
import webbrowser

class IPCheckerApp(wx.App):
    def OnInit(self):
        frame = IPCheckerFrame(None, title="Checker by DedSec", size=(800, 600))
        frame.Show()
        return True

class DetailInfoDialog(wx.Dialog):
    def __init__(self, ip_data, *args, **kwargs):
        super(DetailInfoDialog, self).__init__(*args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)

        ip_label = wx.StaticText(self, label=f"IP: {ip_data.get('ip', 'N/A')}")
        sizer.Add(ip_label, 0, wx.ALL, 10)

        city_label = wx.StaticText(self, label=f"Город: {ip_data.get('city', 'N/A')}")
        sizer.Add(city_label, 0, wx.ALL, 10)

        localhost_label = wx.StaticText(self, label=f"Локальный IP хоста: {socket.gethostbyname(socket.gethostname())}")
        sizer.Add(localhost_label, 0, wx.ALL, 10)

        provider_label = wx.StaticText(self, label=f"Провайдер: {ip_data.get('org', 'N/A')}")
        sizer.Add(provider_label, 0, wx.ALL, 10)

        country_label = wx.StaticText(self, label=f"Страна: {ip_data.get('country', 'N/A')}")
        sizer.Add(country_label, 0, wx.ALL, 10)

        time_label = wx.StaticText(self, label=f"Время: {ip_data.get('timezone', 'N/A')}")
        sizer.Add(time_label, 0, wx.ALL, 10)

        currency_label = wx.StaticText(self, label=f"Валюта: {ip_data.get('currency', 'N/A')}")
        sizer.Add(currency_label, 0, wx.ALL, 10)

        lat_lon_label = wx.StaticText(self, label=f"Широта и долгота: {ip_data.get('loc', 'N/A')}")
        sizer.Add(lat_lon_label, 0, wx.ALL, 10)

        self.SetSizerAndFit(sizer)

    def on_open_gmaps(self, event):
        url = event.GetString()
        webbrowser.open(url)

class IPCheckerFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(IPCheckerFrame, self).__init__(*args, **kw)

        self.SetMinSize((800, 600))
        self.SetMaxSize((800, 600))

        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(139, 0, 0))  # Чёрный фон

        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(panel, label="Программа by DedSec", style=wx.ALIGN_CENTER)
        font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        label.SetFont(font)
        label.SetForegroundColour(wx.Colour(255, 255, 255))
        sizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 20)

        city_label = wx.StaticText(panel, label=f"Город: {self.get_user_city()}", style=wx.ALIGN_CENTER)
        city_label.SetForegroundColour(wx.Colour(255, 255, 255))
        sizer.Add(city_label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 20)

        ip_label = wx.StaticText(panel, label=f"IP: {self.get_user_ip()}", style=wx.ALIGN_CENTER)
        ip_label.SetForegroundColour(wx.Colour(255, 255, 255))
        sizer.Add(ip_label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 20)

        ip_input = wx.TextCtrl(panel)
        sizer.Add(ip_input, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 20)

        check_ip_button = wx.Button(panel, label="поиск по IP")
        check_ip_button.Bind(wx.EVT_BUTTON, lambda event: self.on_check_ip_button(event, ip_input))
        sizer.Add(check_ip_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 20)

        detail_button = wx.Button(panel, label="Проверить информацию о своём IP")
        detail_button.Bind(wx.EVT_BUTTON, self.on_detail_button)
        sizer.Add(detail_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 50)

        rainbow_label = wx.StaticText(panel, label="By DedSec")
        rainbow_label.SetForegroundColour(wx.Colour(0, 255, 0))
        sizer.Add(rainbow_label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 50)

        panel.SetSizer(sizer)

    def get_user_city(self):
        try:
            response = requests.get("https://ipinfo.io/json")
            data = response.json()
            city = data.get("city", "N/A")
            return city
        except requests.exceptions.RequestException:
            return "N/A"

    def get_user_ip(self):
        try:
            response = requests.get("https://ipinfo.io/json")
            data = response.json()
            ip = data.get("ip", "N/A")
            return ip
        except requests.exceptions.RequestException:
            return "N/A"

    def on_check_ip_button(self, event, ip_input):
        entered_ip = ip_input.GetValue()
        if entered_ip:
            ip_data = self.get_ip_info(entered_ip)
            if ip_data:
                self.show_ip_info_dialog(ip_data)
            else:
                wx.MessageBox("Не удалось получить информацию об IP.", "Ошибка", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Введите IP для проверки.", "Предупреждение", wx.OK | wx.ICON_WARNING)

    def on_detail_button(self, event):
        try:
            response = requests.get("https://ipinfo.io/json")
            ip_data = response.json()
            dialog = DetailInfoDialog(ip_data, None, title="Информация об IP")
            dialog.ShowModal()
            dialog.Destroy()
        except requests.exceptions.RequestException:
            wx.MessageBox("Не удалось получить детальную информацию об IP.", "Ошибка", wx.OK | wx.ICON_ERROR)

    def get_ip_info(self, ip):
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            ip_data = response.json()
            return ip_data
        except requests.exceptions.RequestException:
            return None

    def show_ip_info_dialog(self, ip_data):
        dialog = DetailInfoDialog(ip_data, None, title="Информация об IP")
        dialog.ShowModal()
        dialog.Destroy()

if __name__ == "__main__":
    app = IPCheckerApp(False)
    app.MainLoop()
