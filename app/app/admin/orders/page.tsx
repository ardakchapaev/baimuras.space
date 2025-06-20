
'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Plus, 
  Search, 
  Filter, 
  Package,
  DollarSign,
  Clock,
  Truck,
  CheckCircle,
  AlertCircle,
  Eye,
  Edit,
  Printer
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { formatCurrency, formatDate, getStatusColor, getStatusBadge } from '@/lib/utils';
import { Order } from '@/lib/types';

// Mock data
const mockOrders: Order[] = [
  {
    id: '1',
    orderNumber: 'BM240001',
    title: 'Кухонный гарнитур "Модерн"',
    description: 'Полный кухонный гарнитур с островом',
    status: 'in_production',
    totalAmount: 450000,
    paidAmount: 225000,
    discount: 0,
    deliveryDate: new Date('2024-02-15'),
    installationDate: new Date('2024-02-16'),
    createdAt: new Date('2024-01-10'),
    updatedAt: new Date('2024-01-25'),
    orderItems: [],
    payments: [],
    installations: []
  },
  {
    id: '2',
    orderNumber: 'BM240002',
    title: 'Детская мебель Монтессори',
    description: 'Кровать, стол, стеллажи для детской',
    status: 'confirmed',
    totalAmount: 180000,
    paidAmount: 54000,
    discount: 10000,
    deliveryDate: new Date('2024-02-20'),
    createdAt: new Date('2024-01-15'),
    updatedAt: new Date('2024-01-20'),
    orderItems: [],
    payments: [],
    installations: []
  },
  {
    id: '3',
    orderNumber: 'BM240003',
    title: 'Офисная мебель',
    description: 'Столы, стулья, шкафы для офиса',
    status: 'delivered',
    totalAmount: 320000,
    paidAmount: 320000,
    discount: 0,
    deliveryDate: new Date('2024-01-20'),
    installationDate: new Date('2024-01-21'),
    createdAt: new Date('2024-01-05'),
    updatedAt: new Date('2024-01-21'),
    orderItems: [],
    payments: [],
    installations: []
  },
];

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>(mockOrders);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const filteredOrders = orders.filter(order => {
    const matchesSearch = order.orderNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         order.title.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || order.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  const getPaymentProgress = (order: Order) => {
    return (order.paidAmount / order.totalAmount) * 100;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending': return Clock;
      case 'confirmed': return CheckCircle;
      case 'in_production': return Package;
      case 'ready': return Truck;
      case 'delivered': return CheckCircle;
      case 'completed': return CheckCircle;
      case 'cancelled': return AlertCircle;
      default: return Clock;
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
          <h1 className="text-2xl font-bold text-slate-900">Управление заказами</h1>
          <p className="text-slate-600">Отслеживание заказов и их статусов</p>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="outline" size="sm">
            <Printer className="h-4 w-4 mr-2" />
            Отчет
          </Button>
          <Button size="sm">
            <Plus className="h-4 w-4 mr-2" />
            Новый заказ
          </Button>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-slate-900">{orders.length}</div>
            <p className="text-sm text-slate-600">Всего заказов</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-blue-600">
              {orders.filter(o => ['confirmed', 'in_production', 'ready'].includes(o.status)).length}
            </div>
            <p className="text-sm text-slate-600">В работе</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-green-600">
              {formatCurrency(orders.reduce((acc, o) => acc + o.totalAmount, 0))}
            </div>
            <p className="text-sm text-slate-600">Общая сумма</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-purple-600">
              {formatCurrency(orders.reduce((acc, o) => acc + o.paidAmount, 0))}
            </div>
            <p className="text-sm text-slate-600">Оплачено</p>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card>
          <CardContent className="p-4">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
                <Input
                  placeholder="Поиск по номеру заказа или названию..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger className="w-full md:w-48">
                  <SelectValue placeholder="Статус" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Все статусы</SelectItem>
                  <SelectItem value="pending">Ожидает</SelectItem>
                  <SelectItem value="confirmed">Подтвержден</SelectItem>
                  <SelectItem value="in_production">В производстве</SelectItem>
                  <SelectItem value="ready">Готов</SelectItem>
                  <SelectItem value="delivered">Доставлен</SelectItem>
                  <SelectItem value="completed">Завершен</SelectItem>
                  <SelectItem value="cancelled">Отменен</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Orders Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Список заказов ({filteredOrders.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Номер заказа</TableHead>
                  <TableHead>Название</TableHead>
                  <TableHead>Статус</TableHead>
                  <TableHead>Сумма</TableHead>
                  <TableHead>Оплата</TableHead>
                  <TableHead>Доставка</TableHead>
                  <TableHead>Действия</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredOrders.map((order) => {
                  const StatusIcon = getStatusIcon(order.status);
                  const paymentProgress = getPaymentProgress(order);
                  
                  return (
                    <TableRow key={order.id}>
                      <TableCell>
                        <div className="font-medium">{order.orderNumber}</div>
                        <div className="text-sm text-slate-500">
                          {formatDate(order.createdAt)}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="max-w-48">
                          <div className="font-medium truncate">{order.title}</div>
                          <div className="text-sm text-slate-500 truncate">
                            {order.description}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <StatusIcon className="h-4 w-4 text-slate-400" />
                          <Badge className={getStatusColor(order.status)}>
                            {getStatusBadge(order.status)}
                          </Badge>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="text-right">
                          <div className="font-medium">
                            {formatCurrency(order.totalAmount)}
                          </div>
                          {order.discount > 0 && (
                            <div className="text-sm text-green-600">
                              Скидка: {formatCurrency(order.discount)}
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1">
                          <div className="flex items-center justify-between text-sm">
                            <span>{formatCurrency(order.paidAmount)}</span>
                            <span className="text-slate-500">{paymentProgress.toFixed(0)}%</span>
                          </div>
                          <Progress value={paymentProgress} className="h-2" />
                        </div>
                      </TableCell>
                      <TableCell>
                        {order.deliveryDate ? (
                          <div className="text-sm">
                            <div>{formatDate(order.deliveryDate)}</div>
                            {order.installationDate && (
                              <div className="text-slate-500">
                                Установка: {formatDate(order.installationDate)}
                              </div>
                            )}
                          </div>
                        ) : (
                          <span className="text-slate-400">Не назначена</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <Button variant="ghost" size="sm">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <Printer className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Быстрые действия</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <Plus className="h-6 w-6" />
                <span className="text-sm">Новый заказ</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <DollarSign className="h-6 w-6" />
                <span className="text-sm">Добавить оплату</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <Truck className="h-6 w-6" />
                <span className="text-sm">Назначить доставку</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <Printer className="h-6 w-6" />
                <span className="text-sm">Печать документов</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
