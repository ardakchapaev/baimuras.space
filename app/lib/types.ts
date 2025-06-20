
// Types for BaiMuras Furniture Admin Panel

export interface User {
  id: string;
  username: string;
  email: string;
  name?: string;
  phone?: string;
  avatar?: string;
  createdAt: Date;
  updatedAt: Date;
  roles: UserRole[];
}

export interface UserRole {
  id: string;
  userId: string;
  roleId: string;
  role: Role;
}

export interface Role {
  id: string;
  name: string;
  description?: string;
  permissions?: any;
}

export interface Lead {
  id: string;
  name: string;
  email: string;
  phone?: string;
  subject?: string;
  message?: string;
  status: 'new' | 'contacted' | 'qualified' | 'converted' | 'lost';
  score: number;
  source?: string;
  createdAt: Date;
  updatedAt: Date;
  projects: Project[];
}

export interface Project {
  id: string;
  title: string;
  description?: string;
  projectType?: 'furniture' | 'design' | 'academy';
  status: 'planning' | 'in_progress' | 'completed' | 'cancelled';
  budget?: number;
  startDate?: Date;
  endDate?: Date;
  leadId?: string;
  assignedUserId?: string;
  createdAt: Date;
  updatedAt: Date;
  lead?: Lead;
  assignedUser?: User;
  orders: Order[];
  estimates: Estimate[];
  measurements: Measurement[];
  projectImages: ProjectImage[];
}

export interface ProjectImage {
  id: string;
  projectId: string;
  imageUrl: string;
  caption?: string;
  isPrimary: boolean;
  createdAt: Date;
}

export interface Order {
  id: string;
  orderNumber: string;
  title: string;
  description?: string;
  status: 'pending' | 'confirmed' | 'in_production' | 'ready' | 'delivered' | 'completed' | 'cancelled';
  totalAmount: number;
  paidAmount: number;
  discount: number;
  deliveryDate?: Date;
  installationDate?: Date;
  projectId?: string;
  assignedUserId?: string;
  createdAt: Date;
  updatedAt: Date;
  project?: Project;
  assignedUser?: User;
  orderItems: OrderItem[];
  payments: Payment[];
  installations: Installation[];
}

export interface OrderItem {
  id: string;
  orderId: string;
  materialId?: string;
  description: string;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
  material?: Material;
}

export interface Estimate {
  id: string;
  title: string;
  description?: string;
  totalAmount: number;
  validUntil?: Date;
  status: 'draft' | 'sent' | 'approved' | 'rejected' | 'expired';
  notes?: string;
  projectId?: string;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
  project?: Project;
  user: User;
  estimateItems: EstimateItem[];
}

export interface EstimateItem {
  id: string;
  estimateId: string;
  description: string;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
}

export interface Material {
  id: string;
  name: string;
  description?: string;
  category: string;
  unit: string;
  unitPrice: number;
  stockLevel: number;
  minStock: number;
  supplierInfo?: any;
  createdAt: Date;
  updatedAt: Date;
}

export interface Measurement {
  id: string;
  title: string;
  description?: string;
  scheduledAt: Date;
  duration: number;
  status: 'scheduled' | 'completed' | 'cancelled' | 'rescheduled';
  address?: string;
  notes?: string;
  projectId?: string;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
  project?: Project;
  user: User;
}

export interface Payment {
  id: string;
  orderId: string;
  amount: number;
  paymentMethod: string;
  status: 'pending' | 'completed' | 'failed' | 'refunded';
  transactionId?: string;
  notes?: string;
  paidAt?: Date;
  createdAt: Date;
}

export interface Installation {
  id: string;
  orderId: string;
  scheduledAt: Date;
  completedAt?: Date;
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  team?: string;
  notes?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Supplier {
  id: string;
  name: string;
  contactPerson?: string;
  email?: string;
  phone?: string;
  address?: string;
  paymentTerms?: string;
  deliveryTerms?: string;
  rating?: number;
  notes?: string;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

// Dashboard Analytics Types
export interface DashboardStats {
  totalRevenue: number;
  totalOrders: number;
  activeProjects: number;
  pendingLeads: number;
  revenueGrowth: number;
  ordersGrowth: number;
  projectsGrowth: number;
  leadsGrowth: number;
}

export interface RevenueData {
  month: string;
  revenue: number;
  orders: number;
}

export interface ProjectStatusData {
  status: string;
  count: number;
  percentage: number;
}

export interface RecentActivity {
  id: string;
  type: 'order' | 'project' | 'lead' | 'payment';
  title: string;
  description: string;
  timestamp: Date;
  status?: string;
}
