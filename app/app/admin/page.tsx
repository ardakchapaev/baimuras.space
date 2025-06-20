
'use client';

import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  DollarSign, 
  ShoppingCart, 
  FolderOpen, 
  Users,
  TrendingUp,
  Calendar,
  AlertCircle
} from 'lucide-react';
import { StatsCard } from '@/components/dashboard/stats-card';
import { RevenueChart } from '@/components/dashboard/revenue-chart';
import { RecentActivities } from '@/components/dashboard/recent-activities';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { formatCurrency, getStatusColor, getStatusBadge } from '@/lib/utils';

// Mock data - in real app this would come from API
const mockStats = {
  totalRevenue: 2450000,
  totalOrders: 156,
  activeProjects: 23,
  pendingLeads: 12,
  revenueGrowth: 12.5,
  ordersGrowth: 8.3,
  projectsGrowth: 15.2,
  leadsGrowth: -2.1,
};

const mockRevenueData = [
  { month: 'Янв', revenue: 180000, orders: 12 },
  { month: 'Фев', revenue: 220000, orders: 15 },
  { month: 'Мар', revenue: 310000, orders: 20 },
  { month: 'Апр', revenue: 290000, orders: 18 },
  { month: 'Май', revenue: 340000, orders: 22 },
  { month: 'Июн', revenue: 420000, orders: 28 },
];

const mockActivities = [
  {
    id: '1',
    type: 'order' as const,
    title: 'Новый заказ #BM240001',
    description: 'Кухонный гарнитур для семьи Джумабековых',
    timestamp: new Date(Date.now() - 1000 * 60 * 30),
    status: 'pending'
  },
  {
    id: '2',
    type: 'project' as const,
    title: 'Проект "Современная спальня"',
    description: 'Завершен этап планирования',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2),
    status: 'in_progress'
  },
  {
    id: '3',
    type: 'payment' as const,
    title: 'Оплата заказа #BM239985',
    description: 'Получен платеж 150,000 сом',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4),
    status: 'completed'
  },
  {
    id: '4',
    type: 'lead' as const,
    title: 'Новая заявка',
    description: 'Анна Петрова интересуется детской мебелью',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 6),
    status: 'new'
  },
];

const mockUpcomingTasks = [
  {
    id: '1',
    title: 'Замер у клиента Иванов',
    time: '10:00',
    type: 'measurement',
    priority: 'high'
  },
  {
    id: '2',
    title: 'Доставка заказа #BM239980',
    time: '14:00',
    type: 'delivery',
    priority: 'medium'
  },
  {
    id: '3',
    title: 'Встреча с поставщиком',
    time: '16:30',
    type: 'meeting',
    priority: 'low'
  },
];

export default function AdminDashboard() {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-gradient-to-r from-teal-500 to-teal-600 rounded-2xl p-6 text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">
              Добро пожаловать в админ панель BaiMuras
            </h1>
            <p className="text-teal-100">
              {currentTime.toLocaleDateString('ru-RU', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold">
              {currentTime.toLocaleTimeString('ru-RU', { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </div>
            <p className="text-teal-100 text-sm">Текущее время</p>
          </div>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Общая выручка"
          value={formatCurrency(mockStats.totalRevenue)}
          change={mockStats.revenueGrowth}
          changeLabel="за месяц"
          icon={DollarSign}
          color="green"
          index={0}
        />
        <StatsCard
          title="Всего заказов"
          value={mockStats.totalOrders}
          change={mockStats.ordersGrowth}
          changeLabel="за месяц"
          icon={ShoppingCart}
          color="blue"
          index={1}
        />
        <StatsCard
          title="Активные проекты"
          value={mockStats.activeProjects}
          change={mockStats.projectsGrowth}
          changeLabel="за месяц"
          icon={FolderOpen}
          color="purple"
          index={2}
        />
        <StatsCard
          title="Новые заявки"
          value={mockStats.pendingLeads}
          change={mockStats.leadsGrowth}
          changeLabel="за месяц"
          icon={Users}
          color="orange"
          index={3}
        />
      </div>

      {/* Charts and Activities */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <RevenueChart data={mockRevenueData} />
        </div>
        <div>
          <RecentActivities activities={mockActivities} />
        </div>
      </div>

      {/* Today's Tasks and Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Today's Tasks */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card className="bg-white border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Calendar className="h-5 w-5 text-teal-500" />
                <span>Задачи на сегодня</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {mockUpcomingTasks.map((task, index) => (
                  <motion.div
                    key={task.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                    className="flex items-center justify-between p-3 rounded-lg hover:bg-slate-50 transition-colors"
                  >
                    <div className="flex-1">
                      <h4 className="text-sm font-medium text-slate-900">
                        {task.title}
                      </h4>
                      <p className="text-sm text-slate-500">{task.time}</p>
                    </div>
                    <Badge
                      variant={task.priority === 'high' ? 'destructive' : 
                              task.priority === 'medium' ? 'default' : 'secondary'}
                    >
                      {task.priority === 'high' ? 'Высокий' :
                       task.priority === 'medium' ? 'Средний' : 'Низкий'}
                    </Badge>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <Card className="bg-white border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5 text-teal-500" />
                <span>Быстрые действия</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-3">
                <Button 
                  variant="outline" 
                  className="h-20 flex flex-col items-center justify-center space-y-2"
                >
                  <Users className="h-5 w-5" />
                  <span className="text-xs">Новый клиент</span>
                </Button>
                <Button 
                  variant="outline" 
                  className="h-20 flex flex-col items-center justify-center space-y-2"
                >
                  <ShoppingCart className="h-5 w-5" />
                  <span className="text-xs">Создать заказ</span>
                </Button>
                <Button 
                  variant="outline" 
                  className="h-20 flex flex-col items-center justify-center space-y-2"
                >
                  <FolderOpen className="h-5 w-5" />
                  <span className="text-xs">Новый проект</span>
                </Button>
                <Button 
                  variant="outline" 
                  className="h-20 flex flex-col items-center justify-center space-y-2"
                >
                  <Calendar className="h-5 w-5" />
                  <span className="text-xs">Замер</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Alerts */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <Card className="bg-orange-50 border-orange-200 shadow-lg">
          <CardContent className="p-4">
            <div className="flex items-center space-x-3">
              <AlertCircle className="h-5 w-5 text-orange-500" />
              <div>
                <h4 className="text-sm font-medium text-orange-800">
                  Требуют внимания
                </h4>
                <p className="text-sm text-orange-700">
                  3 заказа ожидают подтверждения, 2 проекта приближаются к дедлайну
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
