
'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Plus, 
  Search, 
  Filter, 
  Calendar,
  DollarSign,
  User,
  Eye,
  Edit,
  Image
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { formatCurrency, formatDate, getStatusColor, getStatusBadge } from '@/lib/utils';
import { Project } from '@/lib/types';

// Mock data
const mockProjects: Project[] = [
  {
    id: '1',
    title: 'Современная кухня для семьи Ивановых',
    description: 'Полная реконструкция кухни с современным дизайном',
    projectType: 'furniture',
    status: 'in_progress',
    budget: 450000,
    startDate: new Date('2024-01-15'),
    endDate: new Date('2024-03-01'),
    createdAt: new Date('2024-01-10'),
    updatedAt: new Date('2024-01-20'),
    orders: [],
    estimates: [],
    measurements: [],
    projectImages: [
      {
        id: '1',
        projectId: '1',
        imageUrl: 'https://i.pinimg.com/originals/ea/58/05/ea58054fdec0465750e444a093332b77.jpg',
        caption: 'Эскиз кухни',
        isPrimary: true,
        createdAt: new Date()
      }
    ]
  },
  {
    id: '2',
    title: 'Детская комната Монтессори',
    description: 'Безопасная мебель для развития ребенка по методике Монтессори',
    projectType: 'furniture',
    status: 'planning',
    budget: 280000,
    startDate: new Date('2024-02-01'),
    endDate: new Date('2024-02-28'),
    createdAt: new Date('2024-01-25'),
    updatedAt: new Date('2024-01-26'),
    orders: [],
    estimates: [],
    measurements: [],
    projectImages: []
  },
  {
    id: '3',
    title: 'Офисная мебель для IT-компании',
    description: 'Эргономичные рабочие места для команды разработчиков',
    projectType: 'furniture',
    status: 'completed',
    budget: 680000,
    startDate: new Date('2023-12-01'),
    endDate: new Date('2024-01-15'),
    createdAt: new Date('2023-11-20'),
    updatedAt: new Date('2024-01-15'),
    orders: [],
    estimates: [],
    measurements: [],
    projectImages: []
  },
];

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>(mockProjects);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || project.status === statusFilter;
    const matchesType = typeFilter === 'all' || project.projectType === typeFilter;
    
    return matchesSearch && matchesStatus && matchesType;
  });

  const getProgressPercentage = (project: Project) => {
    if (project.status === 'completed') return 100;
    if (project.status === 'cancelled') return 0;
    if (project.status === 'planning') return 25;
    if (project.status === 'in_progress') return 65;
    return 0;
  };

  const getTypeLabel = (type: string) => {
    const types: Record<string, string> = {
      furniture: 'Мебель',
      design: 'Дизайн',
      academy: 'Обучение'
    };
    return types[type] || type;
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
          <h1 className="text-2xl font-bold text-slate-900">Управление проектами</h1>
          <p className="text-slate-600">Отслеживание и управление мебельными проектами</p>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="outline" size="sm">
            <Filter className="h-4 w-4 mr-2" />
            Фильтры
          </Button>
          <Button size="sm">
            <Plus className="h-4 w-4 mr-2" />
            Новый проект
          </Button>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-slate-900">{projects.length}</div>
            <p className="text-sm text-slate-600">Всего проектов</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-blue-600">
              {projects.filter(p => p.status === 'in_progress').length}
            </div>
            <p className="text-sm text-slate-600">В работе</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-green-600">
              {projects.filter(p => p.status === 'completed').length}
            </div>
            <p className="text-sm text-slate-600">Завершено</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-purple-600">
              {formatCurrency(projects.reduce((acc, p) => acc + (p.budget || 0), 0))}
            </div>
            <p className="text-sm text-slate-600">Общий бюджет</p>
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
                  placeholder="Поиск проектов..."
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
                  <SelectItem value="planning">Планирование</SelectItem>
                  <SelectItem value="in_progress">В работе</SelectItem>
                  <SelectItem value="completed">Завершено</SelectItem>
                  <SelectItem value="cancelled">Отменено</SelectItem>
                </SelectContent>
              </Select>
              <Select value={typeFilter} onValueChange={setTypeFilter}>
                <SelectTrigger className="w-full md:w-48">
                  <SelectValue placeholder="Тип" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Все типы</SelectItem>
                  <SelectItem value="furniture">Мебель</SelectItem>
                  <SelectItem value="design">Дизайн</SelectItem>
                  <SelectItem value="academy">Обучение</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Projects Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        {filteredProjects.map((project, index) => (
          <motion.div
            key={project.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <Card className="hover:shadow-lg transition-all duration-300">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg font-semibold text-slate-900 line-clamp-2">
                      {project.title}
                    </CardTitle>
                    <p className="text-sm text-slate-600 mt-1 line-clamp-2">
                      {project.description}
                    </p>
                  </div>
                  {project.projectImages.length > 0 && (
                    <div className="ml-3">
                      <div className="w-12 h-12 bg-slate-100 rounded-lg flex items-center justify-center">
                        <Image className="h-6 w-6 text-slate-400" />
                      </div>
                    </div>
                  )}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Status and Type */}
                <div className="flex items-center justify-between">
                  <Badge className={getStatusColor(project.status)}>
                    {getStatusBadge(project.status)}
                  </Badge>
                  <Badge variant="outline">
                    {getTypeLabel(project.projectType || '')}
                  </Badge>
                </div>

                {/* Progress */}
                <div>
                  <div className="flex items-center justify-between text-sm mb-2">
                    <span className="text-slate-600">Прогресс</span>
                    <span className="font-medium">{getProgressPercentage(project)}%</span>
                  </div>
                  <Progress value={getProgressPercentage(project)} className="h-2" />
                </div>

                {/* Project Details */}
                <div className="space-y-2">
                  {project.budget && (
                    <div className="flex items-center text-sm">
                      <DollarSign className="h-4 w-4 text-slate-400 mr-2" />
                      <span className="text-slate-600">Бюджет:</span>
                      <span className="font-medium ml-1">{formatCurrency(project.budget)}</span>
                    </div>
                  )}
                  {project.startDate && (
                    <div className="flex items-center text-sm">
                      <Calendar className="h-4 w-4 text-slate-400 mr-2" />
                      <span className="text-slate-600">Начало:</span>
                      <span className="ml-1">{formatDate(project.startDate)}</span>
                    </div>
                  )}
                  {project.endDate && (
                    <div className="flex items-center text-sm">
                      <Calendar className="h-4 w-4 text-slate-400 mr-2" />
                      <span className="text-slate-600">Завершение:</span>
                      <span className="ml-1">{formatDate(project.endDate)}</span>
                    </div>
                  )}
                </div>

                {/* Actions */}
                <div className="flex items-center justify-between pt-2 border-t">
                  <div className="flex items-center space-x-2">
                    <Button variant="ghost" size="sm">
                      <Eye className="h-4 w-4 mr-1" />
                      Просмотр
                    </Button>
                    <Button variant="ghost" size="sm">
                      <Edit className="h-4 w-4 mr-1" />
                      Редактировать
                    </Button>
                  </div>
                  {project.assignedUser && (
                    <div className="flex items-center text-sm text-slate-600">
                      <User className="h-4 w-4 mr-1" />
                      <span>Ответственный</span>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </motion.div>

      {filteredProjects.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="text-center py-12"
        >
          <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Search className="h-8 w-8 text-slate-400" />
          </div>
          <h3 className="text-lg font-medium text-slate-900 mb-2">Проекты не найдены</h3>
          <p className="text-slate-600">Попробуйте изменить параметры поиска</p>
        </motion.div>
      )}
    </div>
  );
}
