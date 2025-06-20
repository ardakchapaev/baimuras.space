
'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Settings as SettingsIcon,
  Users,
  Shield,
  Database,
  Bell,
  Palette,
  Mail,
  Server,
  Save,
  Key
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Textarea } from '@/components/ui/textarea';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table';
import { useToast } from '@/hooks/use-toast';

// Mock data for users
const mockUsers = [
  {
    id: '1',
    username: 'admin',
    email: 'admin@baimuras.space',
    name: 'Администратор',
    roles: ['admin'],
    isActive: true,
    lastLogin: new Date('2024-02-01T10:30:00')
  },
  {
    id: '2',
    username: 'manager1',
    email: 'manager1@baimuras.space',
    name: 'Марат Джумабаев',
    roles: ['manager'],
    isActive: true,
    lastLogin: new Date('2024-02-01T09:15:00')
  },
  {
    id: '3',
    username: 'designer1',
    email: 'designer@baimuras.space',
    name: 'Анна Петрова',
    roles: ['designer'],
    isActive: false,
    lastLogin: new Date('2024-01-28T16:45:00')
  },
];

const settingsTabs = [
  { id: 'general', label: 'Общие', icon: SettingsIcon },
  { id: 'users', label: 'Пользователи', icon: Users },
  { id: 'security', label: 'Безопасность', icon: Shield },
  { id: 'notifications', label: 'Уведомления', icon: Bell },
  { id: 'backup', label: 'Резервное копирование', icon: Database },
];

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('general');
  const [users, setUsers] = useState(mockUsers);
  const [settings, setSettings] = useState({
    companyName: 'BaiMuras',
    companyEmail: 'info@baimuras.space',
    companyPhone: '+996 312 123 456',
    companyAddress: 'г. Бишкек, ул. Московская, 123',
    workingHours: '09:00 - 18:00',
    currency: 'KGS',
    taxRate: 12,
    notifications: {
      emailNotifications: true,
      smsNotifications: false,
      pushNotifications: true,
      newOrders: true,
      lowStock: true,
      payments: true,
    },
    security: {
      twoFactorAuth: false,
      sessionTimeout: 30,
      passwordMinLength: 8,
      maxLoginAttempts: 5,
    },
    backup: {
      autoBackup: true,
      backupFrequency: 'daily',
      backupRetention: 30,
    }
  });
  
  const { toast } = useToast();

  const handleSave = () => {
    toast({
      title: 'Настройки сохранены',
      description: 'Изменения успешно применены',
    });
  };

  const toggleUserStatus = (userId: string) => {
    setUsers(prev => prev.map(user => 
      user.id === userId 
        ? { ...user, isActive: !user.isActive }
        : user
    ));
  };

  const renderGeneralSettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Информация о компании</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="companyName">Название компании</Label>
              <Input
                id="companyName"
                value={settings.companyName}
                onChange={(e) => setSettings(prev => ({ ...prev, companyName: e.target.value }))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="companyEmail">Email компании</Label>
              <Input
                id="companyEmail"
                type="email"
                value={settings.companyEmail}
                onChange={(e) => setSettings(prev => ({ ...prev, companyEmail: e.target.value }))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="companyPhone">Телефон</Label>
              <Input
                id="companyPhone"
                value={settings.companyPhone}
                onChange={(e) => setSettings(prev => ({ ...prev, companyPhone: e.target.value }))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="workingHours">Рабочие часы</Label>
              <Input
                id="workingHours"
                value={settings.workingHours}
                onChange={(e) => setSettings(prev => ({ ...prev, workingHours: e.target.value }))}
              />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="companyAddress">Адрес</Label>
            <Textarea
              id="companyAddress"
              value={settings.companyAddress}
              onChange={(e) => setSettings(prev => ({ ...prev, companyAddress: e.target.value }))}
              rows={3}
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Финансовые настройки</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="currency">Валюта</Label>
              <Select value={settings.currency} onValueChange={(value) => setSettings(prev => ({ ...prev, currency: value }))}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="KGS">Сом (KGS)</SelectItem>
                  <SelectItem value="USD">Доллар (USD)</SelectItem>
                  <SelectItem value="EUR">Евро (EUR)</SelectItem>
                  <SelectItem value="RUB">Рубль (RUB)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="taxRate">Налоговая ставка (%)</Label>
              <Input
                id="taxRate"
                type="number"
                value={settings.taxRate}
                onChange={(e) => setSettings(prev => ({ ...prev, taxRate: parseInt(e.target.value) }))}
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderUsersSettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Управление пользователями</CardTitle>
            <Button size="sm">
              <Users className="h-4 w-4 mr-2" />
              Добавить пользователя
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Пользователь</TableHead>
                <TableHead>Роли</TableHead>
                <TableHead>Статус</TableHead>
                <TableHead>Последний вход</TableHead>
                <TableHead>Действия</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>
                    <div>
                      <div className="font-medium">{user.name}</div>
                      <div className="text-sm text-slate-500">{user.email}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex space-x-1">
                      {user.roles.map((role) => (
                        <Badge key={role} variant="outline">
                          {role === 'admin' ? 'Администратор' :
                           role === 'manager' ? 'Менеджер' :
                           role === 'designer' ? 'Дизайнер' : role}
                        </Badge>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center space-x-2">
                      <Switch
                        checked={user.isActive}
                        onCheckedChange={() => toggleUserStatus(user.id)}
                      />
                      <span className={user.isActive ? 'text-green-600' : 'text-red-600'}>
                        {user.isActive ? 'Активен' : 'Заблокирован'}
                      </span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="text-sm text-slate-600">
                      {user.lastLogin.toLocaleString('ru-RU')}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      <Button variant="ghost" size="sm">
                        Изменить
                      </Button>
                      <Button variant="ghost" size="sm" className="text-red-600">
                        Удалить
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );

  const renderSecuritySettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Настройки безопасности</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium">Двухфакторная аутентификация</h4>
              <p className="text-sm text-slate-600">Дополнительная защита учетных записей</p>
            </div>
            <Switch
              checked={settings.security.twoFactorAuth}
              onCheckedChange={(checked) => setSettings(prev => ({
                ...prev,
                security: { ...prev.security, twoFactorAuth: checked }
              }))}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="sessionTimeout">Таймаут сессии (минуты)</Label>
              <Input
                id="sessionTimeout"
                type="number"
                value={settings.security.sessionTimeout}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  security: { ...prev.security, sessionTimeout: parseInt(e.target.value) }
                }))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="passwordMinLength">Минимальная длина пароля</Label>
              <Input
                id="passwordMinLength"
                type="number"
                value={settings.security.passwordMinLength}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  security: { ...prev.security, passwordMinLength: parseInt(e.target.value) }
                }))}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="maxLoginAttempts">Максимум попыток входа</Label>
            <Input
              id="maxLoginAttempts"
              type="number"
              value={settings.security.maxLoginAttempts}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                security: { ...prev.security, maxLoginAttempts: parseInt(e.target.value) }
              }))}
              className="w-48"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderNotificationsSettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Настройки уведомлений</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Email уведомления</h4>
                <p className="text-sm text-slate-600">Получать уведомления на email</p>
              </div>
              <Switch
                checked={settings.notifications.emailNotifications}
                onCheckedChange={(checked) => setSettings(prev => ({
                  ...prev,
                  notifications: { ...prev.notifications, emailNotifications: checked }
                }))}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">SMS уведомления</h4>
                <p className="text-sm text-slate-600">Получать SMS на мобильный телефон</p>
              </div>
              <Switch
                checked={settings.notifications.smsNotifications}
                onCheckedChange={(checked) => setSettings(prev => ({
                  ...prev,
                  notifications: { ...prev.notifications, smsNotifications: checked }
                }))}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Push уведомления</h4>
                <p className="text-sm text-slate-600">Показывать уведомления в браузере</p>
              </div>
              <Switch
                checked={settings.notifications.pushNotifications}
                onCheckedChange={(checked) => setSettings(prev => ({
                  ...prev,
                  notifications: { ...prev.notifications, pushNotifications: checked }
                }))}
              />
            </div>
          </div>

          <div className="border-t pt-6">
            <h4 className="font-medium mb-4">Типы уведомлений</h4>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span>Новые заказы</span>
                <Switch
                  checked={settings.notifications.newOrders}
                  onCheckedChange={(checked) => setSettings(prev => ({
                    ...prev,
                    notifications: { ...prev.notifications, newOrders: checked }
                  }))}
                />
              </div>
              <div className="flex items-center justify-between">
                <span>Низкие остатки на складе</span>
                <Switch
                  checked={settings.notifications.lowStock}
                  onCheckedChange={(checked) => setSettings(prev => ({
                    ...prev,
                    notifications: { ...prev.notifications, lowStock: checked }
                  }))}
                />
              </div>
              <div className="flex items-center justify-between">
                <span>Поступление платежей</span>
                <Switch
                  checked={settings.notifications.payments}
                  onCheckedChange={(checked) => setSettings(prev => ({
                    ...prev,
                    notifications: { ...prev.notifications, payments: checked }
                  }))}
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderBackupSettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Резервное копирование</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium">Автоматическое резервное копирование</h4>
              <p className="text-sm text-slate-600">Создавать резервные копии автоматически</p>
            </div>
            <Switch
              checked={settings.backup.autoBackup}
              onCheckedChange={(checked) => setSettings(prev => ({
                ...prev,
                backup: { ...prev.backup, autoBackup: checked }
              }))}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="backupFrequency">Частота резервного копирования</Label>
              <Select 
                value={settings.backup.backupFrequency} 
                onValueChange={(value) => setSettings(prev => ({
                  ...prev,
                  backup: { ...prev.backup, backupFrequency: value }
                }))}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="daily">Ежедневно</SelectItem>
                  <SelectItem value="weekly">Еженедельно</SelectItem>
                  <SelectItem value="monthly">Ежемесячно</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="backupRetention">Хранить резервные копии (дни)</Label>
              <Input
                id="backupRetention"
                type="number"
                value={settings.backup.backupRetention}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  backup: { ...prev.backup, backupRetention: parseInt(e.target.value) }
                }))}
              />
            </div>
          </div>

          <div className="flex space-x-3">
            <Button variant="outline">
              <Database className="h-4 w-4 mr-2" />
              Создать резервную копию сейчас
            </Button>
            <Button variant="outline">
              <Server className="h-4 w-4 mr-2" />
              Восстановить из копии
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'general': return renderGeneralSettings();
      case 'users': return renderUsersSettings();
      case 'security': return renderSecuritySettings();
      case 'notifications': return renderNotificationsSettings();
      case 'backup': return renderBackupSettings();
      default: return renderGeneralSettings();
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Настройки системы</h1>
          <p className="text-slate-600">Конфигурация и управление параметрами системы</p>
        </div>
        <Button onClick={handleSave}>
          <Save className="h-4 w-4 mr-2" />
          Сохранить изменения
        </Button>
      </motion.div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="lg:w-64"
        >
          <Card>
            <CardContent className="p-4">
              <nav className="space-y-2">
                {settingsTabs.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                        activeTab === tab.id
                          ? 'bg-teal-50 text-teal-700 border border-teal-200'
                          : 'text-slate-600 hover:bg-slate-50'
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                      <span>{tab.label}</span>
                    </button>
                  );
                })}
              </nav>
            </CardContent>
          </Card>
        </motion.div>

        {/* Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="flex-1"
        >
          {renderTabContent()}
        </motion.div>
      </div>
    </div>
  );
}
